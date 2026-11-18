---
title: "Computability and complexity are different questions"
module: "theory-of-computation"
code: "CS 8101"
number: 8
objective: "Separate decision, recognition and practical resource bounds."
---

## What you should be able to do
Separate decision, recognition and practical resource bounds.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A Turing-machine model adds an unbounded tape and a head that can read, write and move. It is a mathematical model, not a claim that real computers have infinite physical memory. A decider halts on every input and answers yes or no. A recognizer must accept members, but may run forever on some nonmembers.

The halting problem asks whether an arbitrary program halts on an arbitrary input. There is no algorithm that correctly decides all such program-input pairs. This does not mean that we can never prove a particular program halts; simple bounded loops are often easy to analyze.

Complexity asks about resource use, such as time or memory, for a solvable task as input size grows. A linear scan has a different growth pattern from checking all subsets. Being computable does not automatically mean being practical. Big-O gives an asymptotic upper bound, not the exact running time on a particular laptop.

Worked comparison: Determining whether a finite binary string ends in 01 is decidable and can be handled by a DFA. Proving that a general-purpose halting checker cannot exist concerns impossibility across all programs. These are fundamentally different kinds of claims.

## Reasoning in more depth
An algorithm can be guaranteed to finish yet require too many steps for a large input. A recognizer for a language is weaker than a decider because it need not terminate on nonmembers. When discussing an impossible general algorithm, specify the universal claim; it does not forbid solving restricted cases. Complexity also requires an input-size model: scanning n characters and scanning every subset of n items are different growth rates.

## Independent task | Attempt before reading the answer
Classify: a DFA simulation on a finite string; exhaustive testing of all subsets of n items; and a proposed checker that decides halting for every program/input pair.

## Worked answer and marking points
A DFA simulation is decidable and can scan a length-n string in O(n) time in the usual model. Exhaustive subset search is finite and thus can terminate, but enumerates 2^n subsets before accounting for per-subset work. A universally correct halting decider is impossible. These illustrate efficiency, termination and impossibility as separate issues.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
