---
layout: post
title: Github and well-known
order: 10
type: markdown
overview: How to use well-known in github
---

Experimenting with github and atproto. Since each github user has a github.io domain - it 
would seem natural to use it as a handle in Bsky, in particular for a 'professional' profile and with relatively strong identity.

This is even more useful for project accounts.

Adding the .well-known/ directory to a github repo didn't work initially. The github.io site is published with Jekyll (usually), and adding to _config.yaml 'include' didn't seem to help. However, [this site](https://github.com/wojtek-kalicinski/wojtek-kalicinski.github.io) suggests `include [".well-known"]` - I was trying the list and without quotes - and it did the trick.


Next step I'm still struggling with is adding the comments based on [Coryzune](https://www.coryzue.com/writing/bluesky-comments/) - I haven't use github pages in a long time and js/css in at least a decade - doesn't seem to have errors but didn't work either. What was missing in his post: `<div id="bluesky-comments"></div>`


<div id="bluesky-comments"></div>

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
