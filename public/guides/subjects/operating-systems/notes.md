# CS 8140 | Operating Systems

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
An operating system coordinates access to hardware and provides abstractions that make programs usable. This module develops a working understanding of processes, scheduling, memory, concurrency, files and protection. Use the eight sessions, paper calculations and a safe shell sandbox. These foundation topics are inferred from the module title, not an official weekly outline.

Prerequisites: the difference between source code and an executable, binary units, and basic C variables and functions. A terminal is an interface to a shell; it is not itself the operating system.

## Session map
1. Abstractions and the kernel
2. Programs, processes and threads
3. Scheduling and performance measures
4. Virtual memory and address translation
5. Allocation, locality and replacement
6. Concurrency, races and synchronization
7. Deadlock and progress
8. Files, permissions and a safe shell lab

# Session 01 | Abstractions and the kernel

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


# Session 03 | Scheduling and performance measures

## What you should be able to do
Calculate turnaround, waiting and response time under stated assumptions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A scheduler chooses among ready work. First-come, first-served uses arrival order. Shortest-job-first favors the shortest known burst in its nonpreemptive form. Round robin gives each ready process a quantum and rotates unfinished work. Real schedulers must balance responsiveness, throughput, fairness and overhead; no single policy is ideal for every workload.

Turnaround time = completion time - arrival time. Response time = first execution time - arrival time. For simple single-burst exercises with no I/O, waiting time = turnaround time - CPU burst. State these assumptions before using that shortcut.

Worked example: All jobs arrive at time 0. A needs 5 units, B needs 3, C needs 1. FCFS in order A,B,C completes them at 5,8,9. Turnaround times are 5,8,9 and waiting times 0,5,8; average waiting is 13/3. SJF runs C,B,A, completing C at 1, B at 4 and A at 9. Waiting times for C,B,A are 0,1,4, averaging 5/3. These numbers depend on the stated arrival pattern and no switching cost.

## Reasoning in more depth
Always state arrival times, burst lengths, scheduling rule and overhead assumptions. Turnaround is completion minus arrival. Response time is first scheduled time minus arrival. In a single-burst example without I/O, waiting equals turnaround minus CPU burst; with several CPU and I/O phases, account for their time separately. A low average can hide one badly delayed job, so inspect individual outcomes as well.

## Independent task | Attempt before reading the answer
Three jobs arrive at time 0 with bursts A=6, B=2, C=1. Under FCFS in order A,B,C, compute completion, waiting and mean waiting. Ignore overhead.

## Worked answer and marking points
Completion times are 6,8,9. Waiting times are 0,6,8, so mean waiting is 14/3 time units. Turnaround equals completion because arrivals are zero. Response equals waiting in this nonpreemptive single-burst case. Reordering changes the result, so the queue order is part of the specification.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 04 | Virtual memory and address translation

## What you should be able to do
Translate a virtual address using page number and offset.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Virtual addresses belong to a process's address space. Hardware and the operating system translate them to physical memory using structures such as page tables. Paging divides the address space into fixed-size pages and physical memory into corresponding frames. The offset identifies a position within a page; the page number identifies which translation to use.

Worked example: With 4096-byte pages, virtual address 10000 has page number floor(10000/4096)=2 and offset 1808. If virtual page 2 maps to physical frame 7, the physical address is 7*4096+1808=30480.

A translation lookaside buffer caches address translations. A page fault means the current access requires operating-system handling; it does not always mean a programming error. A valid page may need loading, while an invalid or prohibited access may lead to a fault signal or termination. Virtual memory does not create unlimited RAM: sustained memory pressure can make a system slow or unable to satisfy requests.

## Reasoning in more depth
With fixed-size pages, division gives the virtual page number and the remainder gives the offset. The page table maps a virtual page to a physical frame. Translation changes the frame part but preserves the offset. A missing resident page may require fault handling; an invalid access may instead be rejected. A page fault is an event requiring OS work, not automatically a programming error.

## Independent task | Attempt before reading the answer
Page size is 1024 bytes. Virtual address 2500 lies in a page mapped to physical frame 7. Find the page number, offset and physical address.

## Worked answer and marking points
2500=2*1024+452, so virtual page=2 and offset=452. Frame 7 starts at 7168; the physical address is 7168+452=7620. The mapping came from the page table, not from assuming virtual page 2 means physical frame 2.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 05 | Allocation, locality and replacement

## What you should be able to do
Trace a replacement policy and explain locality without equating it to a guarantee.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Allocation decides which memory regions are available to programs and how they are tracked. Internal fragmentation is unused space inside an allocated unit; external fragmentation is free space split into separate regions that cannot satisfy a larger contiguous request. Paging addresses some external-contiguity problems but introduces its own costs and internal waste.

Locality explains why caching can work. Temporal locality means recently used data may be used again. Spatial locality means nearby data may be accessed soon. Programs scanning arrays in order often behave differently from programs touching unpredictable addresses.

Worked example: Suppose two frames use FIFO replacement and the reference string is 1,2,1,3,1. Load 1: fault. Load 2: fault. Read 1: hit. Read 3: fault, replacing the oldest loaded page 1. Read 1: fault, replacing page 2. Total: four faults. The hit on page 1 did not refresh its position in FIFO. Under LRU, accesses do update recency; do not confuse the policies.

## Reasoning in more depth
Temporal locality means recently used data tends to be reused; spatial locality means nearby locations tend to be accessed. These are workload tendencies. Under FIFO, eviction follows insertion order and a hit does not refresh that order. Under LRU, a hit changes recency. State the initial frames and policy before counting faults, or apparently different answers may be modeling different systems.

## Independent task | Attempt before reading the answer
With three initially empty frames, trace FIFO on references 1,2,3,1,4,1. List faults and hits.

## Worked answer and marking points
1,2,3 are faults and fill the frames in that order. The next 1 is a hit and does not alter FIFO order. 4 faults and replaces the oldest page 1. The final 1 faults and replaces page 2. Total: five faults, one hit. An LRU trace would differ because the hit refreshes recency.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 06 | Concurrency, races and synchronization

## What you should be able to do
Demonstrate a lost update and state what synchronization must protect.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A race occurs when correctness depends on uncontrolled ordering or timing between concurrent operations. Even a simple increment can involve reading, modifying and writing shared state. A critical section is the part that must be coordinated to preserve an invariant. A mutex can ensure only one participating thread enters a protected region at a time.

Worked example: Shared count starts at 0. Thread A reads 0, thread B reads 0, A writes 1, B writes 1. Two increments have produced 1 rather than 2. Protecting the complete read-modify-write operation with the same mutex prevents that interleaving among threads following the protocol.

A lock should protect a clearly stated invariant, not just an arbitrary line. Condition variables help wait for a predicate while releasing and later reacquiring a related mutex. Predicates are generally checked in a loop because wakeups do not guarantee the desired condition still holds. Semaphores track permits and can support resource limits, but using a semaphore does not by itself make a design correct.

## Reasoning in more depth
An increment usually contains a read, arithmetic and write. If two workers interleave those steps, one can overwrite the other's result. Protect the entire read-modify-write sequence, not just a conveniently chosen line. A mutex provides exclusion under its contract; it does not automatically fix a wrong invariant or prevent deadlock from inconsistent lock ordering. In C, an unsynchronized data race has language-level consequences beyond a simple predictable interleaving.

## Independent task | Attempt before reading the answer
Two abstract workers read counter=10 before either writes. Each adds one locally and writes the result. What value may remain, and what should the protected operation be?

## Worked answer and marking points
Both read 10, compute 11 and write 11, so the abstract interleaving leaves 11 rather than 12. Protect read, increment and write as one synchronized critical operation, or use a suitable atomic increment. This trace is a teaching model, not a promise about behavior of a real C program with a data race.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 07 | Deadlock and progress

## What you should be able to do
Identify a circular wait and compare prevention with detection.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Deadlock is a situation where participants cannot proceed because each waits for resources or actions held up by others. The classic necessary conditions are mutual exclusion, hold-and-wait, no preemption and circular wait. Breaking a necessary condition can prevent this class of deadlock, but the method may impose other costs.

Worked example: A holds lock X and waits for Y; B holds Y and waits for X. Both follow their local plans, but neither can progress. A consistent global lock order, such as always acquiring X before Y, prevents that particular cycle when all participants follow the order.

Starvation is different: a participant waits indefinitely while others continue to make progress. Livelock involves activity without useful progress, such as two participants repeatedly yielding to one another. Describe the observed progress pattern before naming the problem.

Practical rule: minimize the resources held while waiting, define ownership clearly, and avoid assuming that adding more locks automatically improves correctness.

## Reasoning in more depth
Deadlock means a set of participants cannot proceed because each waits for something held within the set. Starvation means a participant keeps being bypassed even while others progress. A lock-order rule prevents a cycle by requiring all participants to acquire resources in the same global order. Detection needs a model of dependencies and a recovery policy; a timeout alone does not prove a deadlock occurred.

## Independent task | Attempt before reading the answer
Worker A holds L1 and requests L2. Worker B holds L2 and requests L1. Show a cycle and propose an ordering repair.

## Worked answer and marking points
Dependencies form A -> B -> A: A needs B to release L2 and B needs A to release L1. Require both workers to acquire L1 before L2. A worker waiting for L1 then holds no L2, breaking this circular-wait pattern. Every code path using the pair must follow the same rule.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 08 | Files, permissions and a safe shell lab

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


## Practice set
1. Explain kernel versus shell in two sentences.
2. Can one program correspond to two processes? Give an example.
3. State a resource threads commonly share and one item each thread needs separately.
4. Why does blocked differ from ready?
5. FCFS: A arrives 0, burst 4; B arrives 1, burst 2; C arrives 2, burst 1. Find completion, turnaround and waiting times. Assume no overhead and no I/O.
6. All arrive at 0: A needs 3, B needs 2. Round robin, quantum 1, starting A then B, no overhead. Give the timeline and completion times.
7. With 1024-byte pages, split address 3500 into page number and offset.
8. If that page maps to frame 5, calculate the physical address.
9. Two frames, FIFO, reference string 1,2,1,2,3. Count faults.
10. Give an interleaving that loses one of two increments from an initial count of 4.
11. Explain a lock-order solution for an X/Y deadlock.
12. Translate mode 750 into owner/group/other permissions. Explain why applying it to a directory is not the same as applying it to a regular file.

## Answers and reasoning
1. The kernel manages resources and protection at a privileged level. A shell reads commands and launches programs or performs its own built-in operations.
2. Yes. Opening two separate instances of the same executable can create two processes with different execution states and resources.
3. Threads share the process address space. Each needs its own stack and execution context, including a program-counter state.
4. A blocked task is waiting for an event such as I/O. A ready task can run when the scheduler assigns execution resources.
5. A runs 0-4, B 4-6, C 6-7. Completion A=4,B=6,C=7. Turnaround 4,5,5. Waiting 0,3,4.
6. A 0-1, B 1-2, A 2-3, B 3-4, A 4-5. B completes at 4; A at 5.
7. 3500=3*1024+428, so page 3, offset 428.
8. 5*1024+428=5548. Frame number replaces page number; offset is preserved.
9. Faults on 1,2,3; hits on the repeated 1 and 2. Total three faults. Page 1 is replaced at the final access.
10. Both read 4; A writes 5; B writes 5. Final 5 rather than 6. The update needs coordination.
11. Require all code needing both locks to acquire X before Y. A participant cannot hold Y while waiting for X under this protocol, breaking the circular pattern.
12. Owner rwx, group r-x, others --- . On a directory, x means traversal and r means listing; on an ordinary file, x means permission to execute, subject to other requirements.

## Further study and evidence
Use the authors' free OSTEP chapters at https://pages.cs.wisc.edu/~remzi/OSTEP/ for deeper treatment. Consult your local man pages for commands on your machine; Linux and macOS details may differ. Produce one annotated scheduling timeline, one address-translation calculation and one terminal transcript from the sandbox. Original explanations and exercises in this pack are not copied from OSTEP.
