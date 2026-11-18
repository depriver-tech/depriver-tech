---
title: "Scheduling and performance measures"
module: "operating-systems"
code: "CS 8140"
number: 3
objective: "Calculate turnaround, waiting and response time under stated assumptions."
---

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
