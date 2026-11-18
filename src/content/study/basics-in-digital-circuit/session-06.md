---
title: "Combinational building blocks"
module: "basics-in-digital-circuit"
code: "CS 8102"
number: 6
objective: "Relate multiplexers and adders to selection and arithmetic functions."
---

## What you should be able to do
Relate multiplexers and adders to selection and arithmetic functions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A combinational circuit's outputs depend on its current inputs, allowing for propagation delay. A multiplexer selects an input according to control bits. A decoder maps an encoded input to selected outputs. Adders combine bits and carries. These blocks compose into larger datapaths.

Worked example: A two-input multiplexer with select S has Y=S'A+SB. If S=0, the expression reduces to A. If S=1, it reduces to B. This derivation is a clearer specification than memorizing a symbol without knowing which input each select value chooses.

A half adder has sum A XOR B and carry AB. A full adder also includes an incoming carry. One expression for its carry is AB + C_in(A XOR B); the sum is A XOR B XOR C_in. Test the all-ones row: 1+1+1=3, so sum=1 and carry=1.

In a ripple-carry adder, carries pass between stages. Correct Boolean outputs do not imply instantaneous operation; the worst-case carry path affects timing.

## Reasoning in more depth
A multiplexer selects among data inputs; its select bits determine which value reaches the output. A half adder combines two one-bit operands with a sum and carry. A full adder includes carry-in, allowing stages to be chained. Distinguish arithmetic weight: a carry contributes to the next higher bit position, so sum and carry cannot be read as two equal-weight outputs.

## Independent task | Attempt before reading the answer
For a full adder with A=1, B=1 and carry-in=1, find sum and carry-out. For a 2:1 mux with D0=0,D1=1, what happens as S changes?

## Worked answer and marking points
The arithmetic total is 3, binary 11: sum=1 and carry-out=1. For the mux, S=0 selects D0=0 and S=1 selects D1=1, so this wiring outputs S. The full-adder result represents sum+2*carry-out=3.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
