# YouTube Video Script
# "I Used AI to Build an AI-Controlled Blender Render Farm (And It Nearly Broke Me)"
# Estimated runtime: 18-22 minutes

---

## THUMBNAIL CONCEPT
- Split image: Claude chat on left, Blender render on right
- Text overlay: "AI + Blender Render Farm"
- Subtext: "Everything They Don't Tell You"
- Colour scheme: Dark background, cyan/orange accent (matches Flamenco dashboard aesthetic)

---

## TITLE OPTIONS (pick one)
1. "I Used AI to Build an AI-Controlled Blender Render Farm (And It Nearly Broke Me)"
2. "Blender MCP + Flamenco Render Farm on Windows 11 — The Real Setup Guide"
3. "Claude AI Controls Blender While My Render Farm Actually Works — Here's How"

---

## DESCRIPTION (paste into YouTube)

I spent two days setting up a Blender render farm on Windows 11 Pro using Flamenco 3.9 and Blender 5.1 — with Claude AI helping debug every step in real time. This video covers everything that went wrong, how we fixed it, and the moment it all clicked.

Also covers Blender MCP — connecting Claude AI directly to Blender so it can control your scene, create objects and set up renders through conversation.

Timestamps:
0:00 — Intro and what we're building
2:00 — What is Blender MCP and why it's a game changer
5:00 — Setting up the Flamenco render farm
8:00 — Everything that went wrong (and there was a lot)
14:00 — The fixes — GPO firewall, missing manifest, yaml battles
18:00 — First successful render — meet Squishy
20:00 — GitHub repo walkthrough and performance tips

GitHub repo with all pre-configured files:
https://github.com/guilderbeast/flamenco-win11-blender5-setup

Chapters, links and resources in the pinned comment.

---

## INTRO (0:00 — 2:00)
### On camera or voiceover over B-roll of Blender

"What you're looking at is a Blender scene being rendered across two computers simultaneously — coordinated by a render farm I set up from scratch on Windows 11 Pro.

But here's the twist — I also connected Claude AI directly into Blender itself, so I can literally have a conversation with my AI and watch it build and modify scenes in real time.

Getting both of those things working took two days, a lot of swearing, and fixing problems that aren't documented anywhere.

This video covers all of it — what these tools are, how to set them up, every wall I hit, and how to get through them faster than I did.

Let's start with the part that genuinely blew my mind."

---

## PART 1 — BLENDER MCP (2:00 — 5:00)
### Screen capture of Claude chat + Blender side by side

"MCP stands for Model Context Protocol. It's a way of connecting AI tools like Claude directly to applications on your computer — so instead of just chatting, the AI can actually DO things.

In Blender's case, that means I can type something like 'create a low poly aircraft scene with three Spitfires in formation' — and watch Blender actually build it.

[DEMO CLIP: Show Claude receiving a prompt and Blender responding in real time]

The setup isn't complicated — it runs a small local server inside Blender that Claude connects to. But the combination of having AI that can understand what you want AND directly execute it inside your 3D software is genuinely one of those moments where you realise things have changed.

I'll do a dedicated deep dive video on Blender MCP separately — for now just know it's running alongside our render farm and it's incredible."

---

## PART 2 — WHAT IS A RENDER FARM (5:00 — 6:30)
### Simple diagram or screen animation

"A render farm is just multiple computers working together to render your animation faster.

Instead of one machine rendering frame 1, then frame 2, then frame 3 — you have two machines where one does the odd frames and one does the even frames. Double the computers, roughly double the speed.

Flamenco is the official Blender Foundation render manager — it's free, open source, and designed specifically for this. One machine runs the Manager — that's the brain that hands out jobs. Every machine including the manager runs a Worker — that's what actually does the rendering.

In theory it's simple. In practice on Windows 11 Pro it's a different story."

---

## PART 3 — THE SETUP THAT SHOULD WORK (6:30 — 8:00)
### Screen capture of Flamenco dashboard

"Here's what the official docs tell you to do:

- Download Flamenco
- Run the manager
- Run the workers
- Install the Blender addon
- Submit a job

And if you're on Linux with a clean environment, that probably works fine.

On Windows 11 Pro with Blender 5.1? Every single one of those steps has a hidden problem waiting for you.

Let me walk you through each one."

---

## PART 4 — EVERYTHING THAT WENT WRONG (8:00 — 14:00)
### Screen capture with talking head or voiceover

### Problem 1 — The Missing Manifest (8:00)
"The first wall. Blender 5.1 introduced a new extensions platform. Every addon now needs a blender_manifest.toml file to install correctly. The Flamenco 3.9 addon doesn't have one.

So when you try to install it you get a cryptic 'missing manifest' error with no explanation of how to fix it.

The fix is straightforward once you know it — you create the manifest file manually and place it alongside the addon files. I've included the exact file in the GitHub repo so you never have to figure this out yourself.

[SHOW: The manifest file contents and folder structure]"

### Problem 2 — The GPO Firewall (9:30)
"This one cost us the most time. Windows 11 Pro has something called Group Policy — it's designed for corporate environments to enforce security settings across machines.

The problem is it can silently override your local firewall rules. You create a rule to allow Flamenco through on port 8080. Windows says 'yes, rule created.' And then completely ignores it because GPO says no.

The diagnosis took hours. The fix took ten seconds — switch Flamenco to port 80 instead. Standard web traffic port. GPO doesn't block it.

[SHOW: The netsh command showing LocalFirewallRules: N/A (GPO-store only)]

That one line in the terminal output was the smoking gun. Once we saw that everything made sense."

### Problem 3 — The Working Directory (11:00)
"Flamenco passes blend file paths to Blender as relative paths. Which means Blender looks for the file relative to wherever the worker was launched from.

If you launch the worker from the wrong folder — say C:\BlenderFarm instead of C:\BlenderFarm\flamenco-3.9-windows-amd64 — Blender looks in the wrong place and reports 'file not found' even though the file is sitting right there.

The fix is in the batch scripts I've written — they always cd into the correct folder before launching. Once you understand why, it's obvious. Getting there was not obvious.

[SHOW: The error log and the correct startup command]"

### Problem 4 — The yaml That Keeps Resetting (12:30)
"Every time the Flamenco setup wizard runs, it overwrites your configuration file. So any custom settings you've added — port number, timeouts, paths — get wiped.

The solution is to run the wizard once, let it generate the yaml, then edit it immediately and never run the wizard again.

The pre-configured yaml in the GitHub repo has all the right settings already. Copy it in, edit your paths, and you're done."

---

## PART 5 — THE FIXES IN ACTION (14:00 — 18:00)
### Screen capture walkthrough

"Let me show you the complete working setup from scratch.

[WALKTHROUGH: Show folder structure, shared network drive, manager startup, workers connecting, both showing Awake in dashboard]

Two machines, both showing awake, farm status idle — meaning ready and waiting for work.

Now let's submit a render.

[SHOW: Blender addon panel, submit to Flamenco, job appearing in dashboard, both workers picking up tasks]

And there it is. Both machines working. Farm status active.

[SHOW: First completed frame appearing in Last Rendered tab]

That right there is the first frame. We called it Squishy.

After two days of fighting firewalls and missing manifests and yaml files — a rendered frame of a WWII airfield scene with Stukas, Hurricanes and a Junkers Ju 52. Rendered across two machines. RTX 4050 on the laptop, RTX 3060 on the desktop. Both running OptiX.

What used to take 14-16 hours on one machine now takes 6-7 hours on two. And that's before we've even started optimising."

---

## PART 6 — GITHUB REPO WALKTHROUGH (18:00 — 20:00)
### Screen capture of GitHub

"Everything I've described is in this GitHub repo — link in the description and pinned comment.

[WALKTHROUGH: Show each file and what it does]

- blender_manifest.toml — drop this in and the missing manifest error disappears
- flamenco-manager.yaml — pre-configured with port 80, 120 minute timeouts, correct paths
- start-manager.bat and start-worker.bat — one click startup, edit your IP address and go
- Full documentation covering addon installation and performance tips

If this saves you the day it took me to figure all this out, drop a star on the repo and share it with anyone you know who's been putting off setting up a render farm because the docs made it look harder than it is."

---

## OUTRO (20:00 — 21:00)
### On camera or voiceover

"Coming up next — a proper deep dive into Blender MCP and what you can actually do when Claude AI has direct control of your Blender scene. The things you can build through conversation alone are genuinely something else.

If you found this useful, subscribe — I'll be covering more real world Blender pipeline stuff, not just the polished tutorials where everything works first time.

Links to everything in the description. See you in the next one."

---

## B-ROLL CHECKLIST
- [ ] Flamenco dashboard with both workers showing Awake
- [ ] Job being submitted from Blender
- [ ] Both workers active on the dashboard
- [ ] First completed frame in Last Rendered tab
- [ ] The rendered scene itself (WWII airfield)
- [ ] Claude chat + Blender side by side (MCP demo)
- [ ] GitHub repo pages
- [ ] CMD windows showing startup sequence
- [ ] Error messages (for the "what went wrong" section)
- [ ] The yaml file in Notepad

---

## TAGS (paste into YouTube)
blender render farm, flamenco blender, blender 5.1, windows 11 render farm, blender MCP, claude AI blender, blender network render, cycles render farm, flamenco tutorial, blender tutorial, blender AI, render farm setup, windows 11 pro blender, blender addon, GPU rendering
