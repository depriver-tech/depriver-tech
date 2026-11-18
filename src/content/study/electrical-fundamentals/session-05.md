---
title: "Kirchhoff's laws and nodal analysis"
module: "electrical-fundamentals"
code: "CS 8103"
number: 5
objective: "Choose a reference node and solve a one-unknown nodal equation."
---

## What you should be able to do
Choose a reference node and solve a one-unknown nodal equation.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Kirchhoff's current law (KCL) balances charge at a node: with consistent signs, currents entering and leaving sum to zero in the lumped-circuit model. Kirchhoff's voltage law (KVL) balances voltage changes around a closed loop under the conditions of that circuit model. Reference directions can be chosen; a negative answer often means the actual direction opposes the chosen reference.

Worked example: A node V connects through 2 kOhm to an ideal 10 V node and through 3 kOhm to ground. Taking currents leaving the unknown node gives (V-10)/2000 + V/3000 = 0. Multiply by 6000: 3(V-10)+2V=0, so 5V=30 and V=6 V. Current from the 10 V node is (10-6)/2000=2 mA, equal to 6/3000 leaving to ground.

A nodal-analysis routine: choose a reference node, label unknown node voltages, write each resistor current as a voltage difference divided by resistance, apply KCL, solve, then check currents and power. The reference node defines zero potential for the calculation; it does not imply zero current everywhere connected to it.

## Reasoning in more depth
A node voltage is relative to a chosen reference, not an absolute property of a point in isolation. Set current directions consistently, express branch currents with Ohm's law and apply Kirchhoff's current law. A negative current result indicates that the actual direction opposes your chosen arrow; it does not automatically mean an algebra error. Substitute the answer into the node equation to check balance.

## Independent task | Attempt before reading the answer
A node V connects to a 10 V node through 2 kOhm and to reference 0 V through 3 kOhm. Write KCL and solve for V.

## Worked answer and marking points
Using outward currents, (V-10)/2000+V/3000=0. Multiplying by 6000 gives 3V-30+2V=0, so V=6 V. Current from the 10 V node is (10-6)/2000=2 mA; current to reference is 6/3000=2 mA. Incoming and outgoing currents agree.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
