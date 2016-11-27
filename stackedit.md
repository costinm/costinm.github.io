---
tags: markdown docker blog
---

# Evaluating [Stackedit](stackedit.io) 

I am looking for an open source a markdown editor running in a browser, for chrome/android.

Stackedit use nodejs at least for some features, but appears it can work offline. It can sync the local browser storage with Google Drive or a private CouchDB or Dropbox. It can publish to Blogger and github among other things - but no Gogs. Blogger support is interesting - I stopped using blogger in large part because of the editor, I write most of my notes in markdown in a private git repository, didn't bother with setting up a convert/publish system - having it integrated may motivate me to cleanup and publish other random notes.

Github integration is simple, doc is uploaded to the specified repository. Let's see what happens if an edit happens
in github...

A docker image is provided that can run on a private domain, nodejs based. Seems to have some collaborative editing if using a CouchDB, including support for private CouchDB when using stackedit.io. 

Seems to support frontmatter and a comments system - the comments get saved in a HTML comment, at the end of the document as "se_discussion_list:JSON", containing 'selectionStart/selectionEnd/comment[]'. Presumably this is integrated in the couch DB support and synced, but didn't test it yet. 

On google drive: the permissions allow it to add new documents to drive, create or open documents explicitly from drive - but it can't see or access any other file. I assume dropbox is similar. Also seems to have a way to publish via ssh - so some random hosting site like dreamhost.

It can import/export local disk - but one file a time. Shouldn't be a problem if files are saved to Drive, but still need to be opened in Stackedit one by one. 

| Table | Supported |
| --- | --- |
| No | auto-indent|

So far I haven't found a good markdown editor except Emacs orgmode that is good with tables.

For editing-in-chrome I also found [Drive Notepad](https://github.com/drivenotepad/app). Both Drive Notepad and Stackedit are based on ace.js - but Stackedit has more integrations with external storage, while Notepad only support Drive, and is much simpler/cleaner as a result. On the other side, Notepad supports most programming languages - as long as the source is stored in google drive.


 
`
