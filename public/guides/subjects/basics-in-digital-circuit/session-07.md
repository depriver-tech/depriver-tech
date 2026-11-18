# Session 07 | State, latches, flip-flops and counters

## What you should be able to do
Trace state changes at a clock edge and distinguish state from input.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A sequential circuit stores state, so its outputs or future behavior can depend on past inputs. A latch is level-sensitive under its control conditions; an edge-triggered flip-flop captures according to a clock edge and its timing requirements. A register groups storage elements, while a counter updates its stored value according to a rule.

Worked example: A two-bit binary counter cycles 00 -> 01 -> 10 -> 11 -> 00. For a synchronous next-state description, the low bit toggles each step; the high bit toggles when the old low bit is 1. Use the old state consistently when deriving next-state equations.

Reset behavior must be specified. Does reset act synchronously with the clock or asynchronously? Which state does it establish? Without these choices, two circuit descriptions may behave differently even if their normal counting sequence agrees.

Do not describe a flip-flop as "always copying the input." Its sampling behavior and clock conditions are the point of the abstraction.

## Reasoning in more depth
A flip-flop samples according to its timing contract, rather than continuously following every input change. For an ideal positive-edge D flip-flop, the next Q is D at the rising edge. Between sampling events the stored state remains unchanged, assuming no active asynchronous control. Real devices also require setup and hold timing; violating those conditions is not represented by a simple ideal truth table.

## Independent task | Attempt before reading the answer
An ideal D flip-flop starts with Q=0. D is 1 at the first rising edge, then becomes 0 before the second rising edge. Give Q just after each edge and between the edges.

## Worked answer and marking points
After the first rising edge Q=1. Changing D to 0 between edges leaves Q=1. After the second rising edge Q=0. This assumes D is stable for the required setup/hold intervals and that no reset or other control is active.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
