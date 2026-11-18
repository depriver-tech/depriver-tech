# Session 08 | State machines, timing and verification

## What you should be able to do
Specify state transitions and check a timing budget with units.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A finite-state controller connects current state and inputs to next state, and possibly to outputs. In a Moore-style description, outputs depend on state; in a Mealy-style description, outputs can depend on state and current input. Specify which model you are using.

Worked example: A traffic-light teaching model has states Red, Green and Amber, with timer events moving Red -> Green -> Amber -> Red. Outputs are encoded by state. Real road-control systems need far more safety and timing logic; this simplified model is for understanding state transitions, not for deployment.

Propagation delay measures the time before an input change affects an output. Setup and hold requirements constrain when data must be stable around a sampling edge. A circuit can be logically correct but fail when timing constraints are violated. Hazards and glitches can occur when paths have different delays.

Verification routine: declare signal meanings, enumerate required input combinations or state transitions, predict outputs, simulate, compare and explain discrepancies. Keep a waveform or truth table as evidence. Changing a wire until the simulator appears quiet is not a substitute for a specification.

## Reasoning in more depth
A synchronous state machine combines a stored current state with combinational next-state logic. Define the reset state and what each input causes in each state, including unexpected cases. Timing analysis includes clock-to-Q delay, combinational delay and destination setup time, with appropriate clock uncertainty. A functionally correct transition table does not prove the circuit can run at an arbitrary clock rate.

## Independent task | Attempt before reading the answer
A path has clock-to-Q 2 ns, combinational delay 6 ns and setup time 1 ns. Ignoring skew and margin, find the minimum period and corresponding maximum frequency.

## Worked answer and marking points
The period must be at least 2+6+1=9 ns. The corresponding upper frequency bound is 1/(9e-9) Hz, about 111.1 MHz. This simplified bound omits skew, uncertainty and other paths; it is not a guaranteed operating frequency for a physical board.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
