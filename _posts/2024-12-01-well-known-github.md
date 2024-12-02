---
layout: post
title: Github and well-known
order: 10
type: markdown
overview: How to use well-known in github
---

Experimenting with github and atproto.

Adding the .well-known/ directory to a github repo didn't work - the github.io site is 
published with Jekyll (usually), and adding to _config.yaml 'include' doesn't seem to help. Using [this site](https://github.com/wojtek-kalicinski/wojtek-kalicinski.github.io)
suggests `include [".well-known"]`

- The well-known (without dot) does work. Might be an alternative verification if .well-known is blocked - better than just adding to the profile, but risky.


Adding comments based on https://www.coryzue.com/writing/bluesky-comments/ -

  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/bluesky-comments@latest/dist/bluesky-comments.umd.js"></script>
<script>
        document.addEventListener('DOMContentLoaded', function() {
            const uri = 'https://bsky.app/profile/costinm.bsky.social/post/3laymuw5et22v';
            if (uri) {
                initBlueskyComments('bluesky-comments', uri);
            }
        });
</script>
