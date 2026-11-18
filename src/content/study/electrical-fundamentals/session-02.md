---
title: "Ohm's law and power"
module: "electrical-fundamentals"
code: "CS 8103"
number: 2
objective: "Use Ohm's law and power with consistent units and assumptions."
---

## What you should be able to do
Use Ohm's law and power with consistent units and assumptions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
For an ohmic resistor in its valid operating conditions, V=IR. Rearranging gives I=V/R and R=V/I. This is not a universal relationship for every component: diodes, for example, do not behave like a constant resistance across all operating points.

Power transferred with the passive sign convention is P=VI, positive when the element absorbs power under the chosen voltage/current reference directions. For a resistor, combine Ohm's law to obtain P=I^2R=V^2/R. Energy over a constant-power interval is E=Pt.

Worked example: A 1.0 kOhm resistor has 5.0 V across it. I=5/1000=0.005 A=5 mA. Its dissipated power is 5*0.005=0.025 W=25 mW. The same result follows from 25/1000. Checking with a second expression can reveal a unit error.

A practical component has a power rating and may have temperature and voltage limits. A calculated current alone is not a complete component-selection procedure. In a paper exercise, state when you assume ideal components and constant temperature.

## Reasoning in more depth
For an ideal ohmic resistor, voltage and current are proportional at the modeled conditions. Real resistance may change with temperature and components have ratings and tolerances. Power can be calculated as VI, I^2R or V^2/R when the resistor relation applies. Agreement between two formulas is a useful arithmetic check but does not verify that an assumed ideal model matches a real component.

## Independent task | Attempt before reading the answer
For an ideal 1.5 kOhm resistor across 6 V, calculate current and power in two ways.

## Worked answer and marking points
R=1500 ohms. I=6/1500=0.004 A=4 mA. P=VI=6*0.004=0.024 W=24 mW. Also P=V^2/R=36/1500=0.024 W. These are paper-model values, not instructions to connect an unknown supply or component.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
