# Session 04 | Parallel circuits and current division

## What you should be able to do
Use a common branch voltage to calculate parallel resistance and currents.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Components are in parallel when they share both connection nodes and therefore have the same voltage across them. For resistors, 1/R_eq = 1/R1 + 1/R2 + ... . Two resistors give R_eq=R1R2/(R1+R2). For positive finite resistances, the equivalent is smaller than the smallest branch resistance.

Worked example: Put 3 kOhm and 6 kOhm across 12 V. Their currents are 4 mA and 2 mA. Total current is 6 mA, so equivalent resistance is 12/0.006=2 kOhm. The parallel formula gives the same result.

In a two-branch resistive current divider, a smaller resistance receives a larger current. If you forget the formula, calculate the common voltage or reason from I=V/R rather than guessing which resistance belongs in the numerator.

For a mixed series-parallel circuit, simplify an identifiable group, redraw the reduced circuit, and repeat. If the topology is not reducible by those patterns, use a more general method such as nodal analysis.

## Reasoning in more depth
Parallel components share the same two nodes, so their voltages match. Currents divide according to conductance: the smaller resistance carries more current under the same voltage. The equivalent resistance of positive parallel resistors is smaller than the smallest branch resistance. That inequality is a quick error check when a reciprocal sum has been inverted incorrectly.

## Independent task | Attempt before reading the answer
Two ideal resistors, 2 kOhm and 6 kOhm, are in parallel across 6 V. Calculate branch currents, total current and equivalent resistance.

## Worked answer and marking points
Branch currents are 6/2000=3 mA and 6/6000=1 mA. Total is 4 mA. Equivalent resistance is 6/0.004=1500 ohms=1.5 kOhm. This is below 2 kOhm, as expected. The current ratio is inverse to the resistance ratio.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
