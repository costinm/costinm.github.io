#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


POSTS_DIR = Path("_posts")
DEFAULT_PDS = "https://bsky.social"


def request_json(method, url, payload=None, token=None):
    body = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method} {url} failed: {error.code} {detail}") from error


def split_front_matter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end].splitlines(), text[end + 5 :]


def yaml_scalar(lines, key):
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*)$")
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        if value and value[0] in "\"'" and value[-1:] == value[0]:
            value = value[1:-1]
        return value
    return ""


def bsky_block(lines):
    for i, line in enumerate(lines):
        if line == "bsky:":
            j = i + 1
            while j < len(lines) and (lines[j].startswith("  ") or not lines[j].strip()):
                j += 1
            return i, j, lines[i:j]
    return None


def bsky_value(lines, key):
    block = bsky_block(lines)
    if not block:
        return ""
    pattern = re.compile(rf"^\s{{2}}{re.escape(key)}:\s*(.*)$")
    for line in block[2][1:]:
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        if value and value[0] in "\"'" and value[-1:] == value[0]:
            value = value[1:-1]
        return value
    return ""


def should_post(lines):
    value = bsky_value(lines, "post").lower()
    return value not in {"false", "no", "0", "off"}


def post_has_uri(lines):
    return bool(bsky_value(lines, "uri"))


def update_bsky(lines, uri, cid, url):
    values = {
        "post": "true",
        "uri": json.dumps(uri),
        "cid": json.dumps(cid),
        "url": json.dumps(url),
    }
    block = bsky_block(lines)
    if not block:
        return lines + ["bsky:"] + [f"  {key}: {value}" for key, value in values.items()]

    start, end, existing = block
    present = set()
    updated = [existing[0]]
    for line in existing[1:]:
        match = re.match(r"^  ([A-Za-z0-9_-]+):", line)
        if match and match.group(1) in values:
            key = match.group(1)
            updated.append(f"  {key}: {values[key]}")
            present.add(key)
        else:
            updated.append(line)
    for key, value in values.items():
        if key not in present:
            updated.append(f"  {key}: {value}")
    return lines[:start] + updated + lines[end:]


def post_url(path, lines, site_url):
    permalink = yaml_scalar(lines, "permalink")
    if permalink:
        return urllib.parse.urljoin(site_url.rstrip("/") + "/", permalink.lstrip("/"))

    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", path.name)
    if not match:
        raise ValueError(f"{path} does not use the expected YYYY-MM-DD-title.md name")
    year, month, day, slug = match.groups()
    return f"{site_url.rstrip('/')}/{year}/{month}/{day}/{slug}/"


def post_text(title, url):
    prefix = "New post: "
    suffix = f"\n\n{url}"
    limit = 300
    room = limit - len(prefix) - len(suffix)
    if room < 20:
        raise ValueError("Post URL is too long for a Bluesky post")
    clean_title = " ".join(title.split())
    if len(clean_title) > room:
        clean_title = clean_title[: room - 1].rstrip() + "..."
    return f"{prefix}{clean_title}{suffix}"


def link_facet(text, url):
    start = text.index(url)
    end = start + len(url)
    return {
        "index": {
            "byteStart": len(text[:start].encode("utf-8")),
            "byteEnd": len(text[:end].encode("utf-8")),
        },
        "features": [
            {
                "$type": "app.bsky.richtext.facet#link",
                "uri": url,
            }
        ],
    }


def web_url(handle, uri):
    rkey = uri.rstrip("/").split("/")[-1]
    return f"https://bsky.app/profile/{handle}/post/{rkey}"


def create_bsky_post(handle, password, pds, title, url):
    session = request_json(
        "POST",
        f"{pds.rstrip('/')}/xrpc/com.atproto.server.createSession",
        {"identifier": handle, "password": password},
    )
    token = session["accessJwt"]
    text = post_text(title, url)
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "facets": [link_facet(text, url)],
        "langs": ["en"],
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    return request_json(
        "POST",
        f"{pds.rstrip('/')}/xrpc/com.atproto.repo.createRecord",
        {
            "repo": handle,
            "collection": "app.bsky.feed.post",
            "record": record,
        },
        token=token,
    )


def main():
    handle = os.environ.get("BSKY_HANDLE", "costinm.bsky.social")
    password = os.environ.get("BSKY_APP_PASSWORD")
    site_url = os.environ.get("SITE_URL", "https://costinm.github.io")
    pds = os.environ.get("BSKY_PDS", DEFAULT_PDS)
    dry_run = os.environ.get("DRY_RUN", "").lower() in {"1", "true", "yes"}

    if not dry_run and not password:
        print("BSKY_APP_PASSWORD is required", file=sys.stderr)
        return 2

    candidates = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines, body = split_front_matter(text)
        if lines is None:
            continue
        if should_post(lines) and not post_has_uri(lines):
            candidates.append((path, lines, body))

    if not candidates:
        print("No posts need Bluesky publishing.")
        return 0

    for path, lines, body in candidates:
        title = yaml_scalar(lines, "title") or path.stem
        url = post_url(path, lines, site_url)
        print(f"Publishing {path} to Bluesky: {title} -> {url}")
        if dry_run:
            continue
        result = create_bsky_post(handle, password, pds, title, url)
        uri = result["uri"]
        cid = result["cid"]
        lines = update_bsky(lines, uri, cid, web_url(handle, uri))
        path.write_text("---\n" + "\n".join(lines) + "\n---\n" + body, encoding="utf-8")
        print(f"Updated {path} with {uri}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

