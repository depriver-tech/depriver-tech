# Session 03 | Series circuits and voltage division

## What you should be able to do
Calculate series current and predict the effect of loading a divider.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Resistors are in series when the same branch current must pass through each without an intervening branch carrying away current. Equivalent resistance is the sum. The voltage across each resistor is its current times its resistance, so the larger resistance receives the larger voltage drop for the same current.

Worked example: A 12 V ideal source drives 2 kOhm and 4 kOhm in series. Equivalent resistance is 6 kOhm, giving I=12/6000=2 mA. Voltage drops are 4 V and 8 V. Their sum is the source voltage.

The unloaded divider relation is V_out=V_in*R_bottom/(R_top+R_bottom), when output is measured across the bottom resistor and no extra load changes the circuit. Adding a load in parallel with the bottom resistor changes the effective bottom resistance. Do not use the unloaded formula unchanged after attaching a significant load.

A circuit's appearance on a drawing can be misleading. Identify nodes and connections rather than deciding "series" because two components are drawn next to each other.

## Reasoning in more depth
In a series path, the same current passes through each element. The total resistance is the sum, and each voltage drop follows its share of the total. The simple unloaded divider formula assumes no additional current leaves the midpoint. A connected load creates a parallel branch with the lower resistor, changing the equivalent resistance and usually reducing that midpoint voltage.

## Independent task | Attempt before reading the answer
A 12 V ideal source feeds two series 3 kOhm resistors. Find the midpoint voltage unloaded. Then connect an ideal 3 kOhm load across the lower resistor in the paper model.

## Worked answer and marking points
Unloaded, equal resistors divide 12 V equally, giving 6 V. With the load, the lower equivalent is 3k||3k=1.5 kOhm. Total is 4.5 kOhm, so midpoint=12*(1.5/4.5)=4 V. The load invalidates the original unloaded ratio.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
