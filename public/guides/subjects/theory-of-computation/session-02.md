# Session 02 | Deterministic finite automata

## What you should be able to do
Use a state invariant to justify a complete DFA.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A DFA has a finite set of states Q, an alphabet Sigma, a transition function delta: Q x Sigma -> Q, a start state q0 and a set F of accepting states. Each state-symbol pair has exactly one next state. A string is accepted if, after consuming all its symbols, the machine is in an accepting state.

Worked example: Recognize binary strings with an even number of 1s. Use E for even and O for odd. Start in E, and make E accepting. Reading 0 leaves the parity unchanged; reading 1 toggles E and O.

| State | Input 0 | Input 1 | Accepting? |
| --- | --- | --- | --- |
| E (start) | E | O | Yes |
| O | O | E | No |

Trace 1011: E -> O -> O -> E -> O, so reject. Trace 1010: E -> O -> O -> E -> E, so accept. Epsilon is accepted because the initial number of 1s is zero, which is even.

## Reasoning in more depth
A state invariant describes what is true after every consumed prefix, including the empty prefix. For parity, the transition on 1 changes parity and the transition on 0 preserves it. Induction has a base case at the start state and a preservation step for each input symbol. This reasoning explains all lengths; a few successful traces only check selected examples.

## Independent task | Attempt before reading the answer
Design a DFA accepting binary strings with an odd number of 1s. Trace 10101 and explain the empty-string decision.

## Worked answer and marking points
Use E and O. Start E; accept only O. On 0 stay, on 1 toggle. For 10101 the trace is E,O,O,E,E,O, so accept. Epsilon ends at E and is rejected. The invariant is parity of the number of 1s consumed, preserved by both transition rules.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
