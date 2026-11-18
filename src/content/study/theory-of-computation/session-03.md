---
title: "State meaning is more useful than guessing circles"
module: "theory-of-computation"
code: "CS 8101"
number: 3
objective: "Derive states from the suffix information required by a specification."
---

## What you should be able to do
Derive states from the suffix information required by a specification.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
When designing a DFA, state what information must be remembered from the prefix already read. For "ends in 01," remember whether the current suffix is empty or irrelevant, is 0, or is 01. These are meanings of states, not just labels.

Worked example: q0 means no useful suffix; q1 means the prefix ends in 0; q2 means it ends in 01. Start in q0 and accept only q2.

| State | Input 0 | Input 1 |
| --- | --- | --- |
| q0 | q1 | q0 |
| q1 | q1 | q2 |
| q2 | q1 | q0 |

Trace 1001: q0 -> q0 -> q1 -> q1 -> q2, so accept. Trace 010: q0 -> q1 -> q2 -> q1, so reject. Repeated zeroes matter: from q1 on 0, stay in q1 because the most recent symbol still gives a useful 0 suffix.

To justify the construction, explain how each transition preserves the stated meaning. Then test short accepted and rejected strings, including epsilon. Tests help find mistakes; an invariant argument explains all input lengths.

## Reasoning in more depth
For suffix recognition, keep the longest suffix of the consumed input that is also a prefix of the target pattern. When the target is 01, the useful partial matches are empty, 0 and 01. A new symbol can destroy a complete match or start a new partial one. Acceptance depends on the state after all input, so reaching an accepting state early does not guarantee the final string is accepted.

## Independent task | Attempt before reading the answer
Use the ends-in-01 DFA to trace 0101 and 011. Explain why they differ despite both containing 01.

## Worked answer and marking points
0101 follows q0,q1,q2,q1,q2 and accepts. 011 follows q0,q1,q2,q0 and rejects. The final 1 in 011 destroys the required suffix. The specification is ends in 01, not contains 01.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
