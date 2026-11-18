---
title: "Concurrency, races and synchronization"
module: "operating-systems"
code: "CS 8140"
number: 6
objective: "Demonstrate a lost update and state what synchronization must protect."
---

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
