---
layout: post
title: Github pages as Bsky handle 
order: 10
type: markdown
overview: How to use a [user].github.io as Bsky handle.
---

I'm experimenting with github and atproto. Since each github user has a github.io 
domain - it would seem natural to use it as a handle in Bsky, in particular for a 'professional' profile and with relatively strong identity/verification.

The github profiles are associated with organizations, there is some vetting before getting permissions in mainstream projects - and some reputation that can be to some extent used in establishing trust. There are of course plenty of fake profiles and malicious actors - but still a bit better trust than a random name.

This is even more useful for popular github projects.

What seems required is adding a .well-known/atproto-did in the [USER].github.io repo,
and configuring Github pages to preserve it.

Adding the .well-known/ directory to a github repo didn't work initially. The github.io site is published with Jekyll (usually), and adding to _config.yaml 'include' didn't seem to help. However, [this site](https://github.com/wojtek-kalicinski/wojtek-kalicinski.github.io) suggests `include [".well-known"]` - I was trying the list and without quotes - and it did the trick.


Next step I'm still struggling with is adding the comments based on [Coryzune](https://www.coryzue.com/writing/bluesky-comments/) - I haven't use github pages in a long time and js/css in at least a decade - doesn't seem to have errors but didn't work either. What was missing in his post: `<div id="..."></div>` - but it doesn't seem to help.


<div id="bluesky-comments"></div>

<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/bluesky-comments@0.4.0/dist/bluesky-comments.umd.js" crossorigin></script>
<script>
        document.addEventListener('DOMContentLoaded', function() {
                console.log("Loaded bsky");
                initBlueskyComments('bluesky-comments', {author:'costinm.bsky.social'});
        });
</script>
