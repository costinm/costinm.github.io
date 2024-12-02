---
layout: post
title: Github and well-known
order: 10
type: markdown
overview: How to use well-known in github
---

Experimenting with github and atproto.


- Adding the .well-known/ directory to a github repo doesn't work - the github.io site is 
published with Jekyll (usually). Adding to _config.yaml 'include' doesn't seem to help.

- The well-known (without dot) does work. Might be an alternative verification if .well-known is blocked - better than just adding to the profile, but risky.


Adding comments based on https://www.coryzue.com/writing/bluesky-comments/ -

<script>
        document.addEventListener('DOMContentLoaded', function() {
            const uri = 'https://bsky.app/profile/costintest.bsky.h.webinf.info/post/3lccbspcq7k2j';
            if (uri) {
                initBlueskyComments('bluesky-comments', uri);
            }
        });
</script>
