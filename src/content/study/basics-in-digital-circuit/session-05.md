---
title: "From truth tables to simplified logic"
module: "basics-in-digital-circuit"
code: "CS 8102"
number: 5
objective: "Construct a sum of products from the rows that require output one."
---

## What you should be able to do
Construct a sum of products from the rows that require output one.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A sum-of-products expression ORs together terms that AND literals. To build one from a truth table, create a minterm for every row whose output is 1. For a row A=0,B=1,C=0, the minterm is A'BC'. Then simplify with algebra or a Karnaugh map when appropriate.

A Karnaugh map places adjacent cells in Gray-code order, so neighboring cells differ by one input bit. Group adjacent 1s into rectangular power-of-two groups, allowing wraparound where the map structure permits it. Larger groups remove more changing variables. A don't-care entry can be used only when the specification genuinely allows either output for that input.

Worked example: For inputs A,B,C, suppose Y=1 for minterms 1,3,5,7 under the binary index order ABC. These are 001,011,101,111. C is 1 in every row, while A and B vary over all combinations. The simplified function is Y=C.

A simplified expression is meaningful only if it still matches every required row. Verify it rather than trusting the visual shape of a group.

## Reasoning in more depth
A minterm is true for exactly one input row. Include each variable uncomplemented when its row value is 1 and complemented when it is 0, then OR the required minterms. Simplification should preserve the full specified truth table. Treat don't-care inputs as unspecified design freedom only when the specification really permits it; silently ignoring inconvenient rows changes the required behavior.

## Independent task | Attempt before reading the answer
For inputs A,B, Y is 1 on rows 01 and 11 only. Write the canonical sum of products and simplify.

## Worked answer and marking points
Y=(NOT A AND B) OR (A AND B). Factor B to obtain B AND (NOT A OR A)=B. The output depends only on B; checking rows 00,01,10,11 gives 0,1,0,1. No row was assumed to be a don't-care.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
