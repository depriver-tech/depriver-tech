---
title: "Abstractions and the kernel"
module: "operating-systems"
code: "CS 8140"
number: 1
objective: "Explain how kernel abstractions support controlled sharing of hardware."
---

## What you should be able to do
Explain how kernel abstractions support controlled sharing of hardware.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
The kernel is the privileged core that manages resources and enforces protection. User applications normally request services through system calls rather than directly controlling devices. Examples include creating a process, reading a file or requesting memory mappings. A library function may wrap a system call, perform work entirely in user space, or do both.

Useful abstractions include a process for executing work, virtual memory for a process's address space, a file for named persistent data and a thread for a stream of execution. Abstractions simplify programming, but their implementation still has costs and limits.

Worked example: A program writes a line to a file. At the application level, this looks like a call to a standard I/O function. Beneath that interface, buffering, kernel calls, filesystem metadata and storage operations may be involved. Returning from a buffered write is not necessarily proof that data has reached durable storage. Distinguish the interface promise from assumptions about its implementation.

## Reasoning in more depth
An operating system supplies interfaces rather than handing every application direct authority over every device. A system call crosses a controlled boundary to request a privileged operation. Libraries may wrap those calls, but a library function is not automatically a system call. The abstraction can differ from the hardware: a process sees an address space, while physical pages may be shared or moved under OS control.

## Independent task | Attempt before reading the answer
An application saves a file. Distinguish application work, library work and a kernel responsibility without naming platform-specific calls.

## Worked answer and marking points
The application decides which data and file name to save. A library may buffer or format the bytes and request an OS operation. The kernel checks permissions and manages the filesystem/device request. Buffering means an application-level write and durable storage are not identical events; exact guarantees depend on the interface used.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
