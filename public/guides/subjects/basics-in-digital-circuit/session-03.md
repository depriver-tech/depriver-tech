# Session 03 | Gates and truth tables

## What you should be able to do
Derive a truth table from a gate expression rather than its visual shape.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
The basic logical operations include NOT, AND, OR and XOR. AND outputs 1 only when both inputs are 1. OR outputs 1 when at least one input is 1. XOR outputs 1 when exactly one of two inputs is 1. NAND negates AND; NOR negates OR; XNOR negates XOR.

| A | B | AND | OR | XOR | NAND |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 |

Worked example: An alarm activates when a door is open AND the system is armed. Let D=door-open and A=armed. The specification is Y=D AND A. A truth table prevents confusing this with OR, which would activate the alarm whenever the system was armed, even with a closed door.

Write the meaning of 0 and 1 for each input before building the table. A label such as "door" alone is ambiguous: does 1 mean open or closed?

## Reasoning in more depth
For n independent binary inputs, a complete truth table has 2^n rows. Evaluate inner expressions first and label intermediate columns when the logic is nested. A gate symbol or expression represents a function, not the physical timing of its implementation. Two ideal circuits with equal truth tables implement the same combinational function even when their propagation delays differ.

## Independent task | Attempt before reading the answer
Build the truth table for Y=NOT(A AND B). Which input rows make Y zero?

## Worked answer and marking points
For inputs 00,01,10,11 the AND outputs are 0,0,0,1 and Y outputs are 1,1,1,0. Only A=1 and B=1 makes Y zero. This is NAND. The negation applies to the entire AND result, not independently to just one input.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
