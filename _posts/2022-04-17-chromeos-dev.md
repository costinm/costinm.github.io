---
layout: post
title: ChromeOS dev mode
published: true
tags: ChromeOS Linux
---

I am using CloudReady and ChromeOS flex on all my laptops and out-of-support Chromebooks. It meets almost all of my needs - 
don't need to worry about upgrades or if they get stolen/lost, I can work on my main computer using remote desktop and
most of the rest I do using the browser.

From time to time I still need a root shell - for network troubleshooting or experiments, and occasionaly to run 
some applications - CloudReady has 'developer mode' enabled by default, but Flex does not and it seems CloudReady
also plans to default to "normal" mode, without root access. 

Thanks to [redit /r/ChromeOSFlex](https://www.reddit.com/r/ChromeOSFlex/) found an easy way to 
[enable dev mode](https://www.reddit.com/r/ChromeOSFlex/comments/swxlz8/tutorial_enable_developer_mode_on_cros/).

TL;DR is to replace cros_legacy and cros_efi with cros_debug in grub.cfg

A maybe simple way to do this that doesn't require booting another OS and so many commands is to use the EFI shell.
The main pain is figuring out the commands - like Grub shell, it is using a weird syntax, but at least it is 
standardised and common:

```shell
Shell> fs0:

fs0:\> cd \efi\boot

fs0:\efi\boot> edit grub.cfg

# Replace and save
# F4 - search cros_efi, answer "no" if editor asks "next", change it to cros_debug, repeat for all 4.
# Or F5 - search/replace
# Ctrl-Q or F3 to exit, answer "yes" to save. F2 also saves

```

The shell has quite a few interesting tools, and can run scripts, redirect to files - it is also a good
option for recovering Linux of grub.cfg is messed up.

Developer mode allows a root access - but I don't think it reduces the security much. 

I assume this will be needed after each upgrade, will see what happens next time.
