---
title: "Nondeterminism and subset construction"
module: "theory-of-computation"
code: "CS 8101"
number: 4
objective: "Carry out a concrete subset construction including an empty subset."
---

## What you should be able to do
Carry out a concrete subset construction including an empty subset.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An NFA may allow several next states for a symbol, or none. Some definitions also permit epsilon transitions that consume no input. A string is accepted when at least one complete path consumes the string and ends in an accepting state. It is not necessary for every path to accept.

Worked example: To recognize strings containing 01 somewhere, an NFA can remain in a scanning state while reading any symbol, branch to a second state after seeing a 0, then enter an accepting state when the next symbol is 1. Once the substring has been found, it may consume remaining symbols in an accepting loop.

Subset construction converts an NFA to a DFA. A DFA state represents a set of possible NFA states. Start with the epsilon closure of the NFA start state; for each symbol, collect reachable states and then take epsilon closure again. A subset is accepting if it contains at least one NFA accepting state. Include the empty subset when it is reachable; it acts as a rejecting sink.

Nondeterminism changes the description, but DFAs and NFAs recognize the same class of languages: the regular languages. This does not mean that every language is regular.

## Reasoning in more depth
Each subset state represents every location the NFA could occupy after the same consumed prefix. Compute a union of outgoing transitions; do not select a single convenient path. An NFA state with no transition contributes nothing. A reachable empty subset loops to itself on every symbol and is rejecting. Epsilon closure is needed only when the NFA definition includes epsilon transitions.

## Independent task | Attempt before reading the answer
Over {a}, let start s have delta(s,a)={s,t}, and t have no outgoing transitions. Only t accepts. Build the reachable DFA subsets and decide epsilon, a and aa.

## Worked answer and marking points
Start subset {s} rejects. On a it reaches {s,t}, which accepts. From {s,t}, a reaches {s,t} again because s branches and t contributes nothing. Thus epsilon rejects, a and aa accept; indeed every positive number of a symbols accepts. No empty subset is reachable in this particular construction.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
