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
