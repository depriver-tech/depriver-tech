# Session 02 | Programs, processes and threads

## What you should be able to do
Distinguish a program file, a process instance and threads sharing a process.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A program is stored instructions and data. A process is an executing instance with execution state and resources. The same executable can run in several processes. Typical process states include running, ready and blocked; specific operating systems use more detailed state models.

A running process may become ready when preempted, blocked when waiting for I/O, and ready again when the event completes. A context switch saves one execution context and restores another. This is overhead needed to share execution resources, not application work itself.

Threads within a process share an address space and many resources, while each thread has its own execution context and stack. Sharing makes communication convenient, but also creates coordination problems. Processes normally have stronger address-space separation, although they can communicate through controlled mechanisms.

Worked example: An editor can have one thread for the interface and another for background indexing. A blocked indexing operation need not stop all useful interface work if the design and runtime allow progress. This does not mean threads automatically make every program faster.

## Reasoning in more depth
A program stored on disk is passive code and data. Starting it creates an execution context with resources and a process identity. Threads in one process typically share its address space and open resources but have separate instruction progress, registers and stacks. Sharing makes communication convenient and also makes unsynchronized updates hazardous. A blocked thread waiting for input is different from a runnable thread waiting to be scheduled.

## Independent task | Attempt before reading the answer
Two instances of one editor are open. Each instance has a UI thread and a background worker. How many processes and threads does this simplified model describe?

## Worked answer and marking points
Two processes and four threads. Each process contains two threads. The executable can be the same file while execution state differs. This is a simplified model: real editors may use additional helper processes or threads, so process inspection is needed before making claims about a specific application.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
