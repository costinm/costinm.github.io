---
layout: post
title: Authenticated transport
tags: atproto mesh
overview: ATproto for transport only
---

ATproto is an 'authenticated transport protocol'. It also claims to be a standard for public conversation and social - just like HTTP was a standard for hypertext. 

My interest is in the transport and general uses of the protocol - social is important, 
as is hypertext, but just like HTTP is now also used for JSON and many other things, there is no reason to limit ATproto to just social uses. I think it would benefit the protocol (and other non-social applications) to validate the separation between a specific use case (social) and the core protocol. 

As 'authenticated transport', we can ignore "app.bsky", "com.atproto.server" and almost all
other schemas used by the social applications, just like a gRPC server using HTTP is not concerned about CSS, HTML or a super specific web application. 

What is left is a (perhaps) simpler variant of the GIT protocol - as transport and synchronization of signed blobs, and the (broadly used) keypairs for signing and authentication.

As an example, will consider  non-social use cases - like 'auth transport
for configs files' or 'auth transport for logs'. Both are important for the security and scalability of servers and expand the 'zero trust' model. 

`com.atproto.sync` is the main transport protocol: `getBlob`, `listBlobs`, `getRepoStatus` and `getRepo` - returning everything `since`.

`listRepos` is used for multitenant servers - and not relevant if you sync a known repo. 

`notifyOfUpdate` is the 'webhook`. Current protocols use 2 main mechanisms for notifications: long-lived 'watch' (like K8S and most pubsub) and 'webhooks'. They are not 
exclusive and one can be bridged to the other, and atproto also defiles a websocket streaming protocol. Note that K8S does not currently have a generic webhook mechanism (mutating webhooks are specialized and 'before save' - I don't think there is a 'post-save' webhook in K8S).

Most of the methods are as expected - worst is 'notifyOfUpdate' which only takes as 
parameter the 'hostname - usually a (multitenant) PDS'. That is not a problem if a PDS implementation assigns a separate FQDN for each user - while the BSky social discovery 
allows and encourages multitenant, it is not a requirement. 

The most simplified implementation of a (non-social) ATproto:

- use only EC256 and web:did (i.e. FQDNs). 
- implement the 'sync' protocol 
- use a 'single tenant' model externally, with the PDS hosted under the user's domain. Implementation can obviously still be multi-tenant, just like web servers can host many domains.

How records get added to the repo in the social app is not relevant - the repo controller can watch K8S or logs and add each record directly or mirror a different repo.

# Key rotation and immutable records

The most important (IMO) part of the protocol is that each object is signed, using a commit 
object with the current key at the time of the signature. The commit object is used to 
derive an immutable ID.

That means if you fetch a repository you need ALL the public keys and the timestamps of 
the rotations to fully verify all the records, or to have and verify the Merkle tree (full
or diff).

If a key is compromised - it can sign fake records with timestamps in the validity period 
of the key. Normally the Merkle tree is used to protect against this - but it works at the 
repo level, can't verify an individual record without having the full repo with the top
commit signed by the current key.

It appears the protocol had a per-record protection against it - the 'prev' field in commit - but current docs indicate it is no longer used. That may be fine for social, where old records are not that important and are replicated by the central servers - but would be realy bad for logs or configs. Fortunately the field is not deprecated, and can be used.

The other consequence is that all the keys ever used in a repo must be available to verify the repo (unless the full Merkle tree is verified). The BSky PLC protocol is providing such storage - but it is a too complex and centralized solution. Instead, each repo can host a (custom) certificate chain - with each key signed by the previous one. Using X509 certificates should work, but with custom verification since most of the old certs will be expired. In this model, the original key ('genesis' key in PLC) acts as root CA, and the first key in the chain is the current signing key.

This is not a major problem if the protocol is used for "recent" records or can resign. In the use case of configs it is possible to resign the repo with the current key, and for the logs use case the signature needs to protect the logs in transit. Other use cases may need to use the 'prev' field.

# XRPC, Lexicon, etc

The actual RPC or schema format are not significant to the semantics of the protocol. The same 'sync' API can be expressed as gRPC proto or OpenAPI - and may use any marshalling and schema, except the 'commit' object that must be CBOR.

# Merkle tree

Just like Git, Atproto is using a Merkle tree - in addition to signing each object. Like DIDs, it sounds like a 'standard' but it is highly specialized format with very strict
requirements. DMverity and many others use the same concept - and have similar inflexible, srict requirements on the data layout and format.

This is a part where using the ATproto SDK or one of the PDS implementations is a good idea and is something that is best left unchanged.

It is a bit unfortunate that current version is no longer using 'prev' and has a hard dependency on the tree.
