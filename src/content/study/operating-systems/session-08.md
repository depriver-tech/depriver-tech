---
title: "Files, permissions and a safe shell lab"
module: "operating-systems"
code: "CS 8140"
number: 8
objective: "Inspect files safely and interpret permissions within a temporary lab."
---

## What you should be able to do
Inspect files safely and interpret permissions within a temporary lab.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A filesystem organizes named data and metadata. A directory maps names to entries; a path identifies a location. An open file descriptor or handle refers to an opened resource. Filesystems and permission models differ, so Linux examples do not imply every operating system has identical behavior.

On Unix-like systems, the common mode bits give read, write and execute permissions for owner, group and others. For directories, execute generally permits traversal, read permits listing names, and write permits changes to directory entries subject to other rules. File deletion depends strongly on the containing directory's permissions, not simply on whether the file itself is writable.

Safe lab: Work only inside a new practice folder. Use pwd to confirm location, mkdir for a directory, printf to create a small text file, cat to read it, and ls -l to inspect permissions. Try chmod 600 on your own practice file. Use ps to inspect your processes without terminating anything. Do not run destructive cleanup commands or change system permissions to complete this lab.

Worked example: Mode 640 is owner read+write (4+2), group read (4), others none (0): rw-r-----. It does not grant execute permission. A script's executable bit and its interpreter are separate considerations.

## Reasoning in more depth
Use a newly created practice directory and synthetic files. Predict what a command should change, inspect the current directory, then run only the required operation. File content and metadata are different: a listing can show names and permissions without showing contents. Permissions are interpreted under a platform model, so symbolic modes and ownership need local manual pages. Do not test commands on personal documents or university records.

## Independent task | Attempt before reading the answer
Create a paper plan for a shell lab that makes a practice file, lists it, reads it and cleans up only that file. Include a checkpoint before cleanup.

## Worked answer and marking points
Plan: create a unique temporary directory using the local OS tool, enter it, create a synthetic note, list the directory and read the note. Before cleanup, print the current directory and list the exact file name. Remove only the named practice file and then the empty practice directory. Avoid recursive deletion, wildcard removal and commands requiring administrator access.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
