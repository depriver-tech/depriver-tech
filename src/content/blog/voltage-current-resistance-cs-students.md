---
title: "Voltage, current and resistance: three calculations for CS students"
description: "Practise units, Ohm's law, series voltage drops and parallel currents with three worked examples and independent questions."
date: 2026-11-18
status: live
tags: ["students", "study", "electronics"]
---

Electrical fundamentals becomes less mysterious when each quantity has a meaning and every calculation keeps its units.

Voltage describes energy per unit charge. Current describes the rate of charge flow. Resistance relates voltage and current for an ohmic resistor under its applicable operating conditions. They are related quantities, not interchangeable names for electricity.

*Anza na mchoro, andika units, halafu tumia formula.* Start with the circuit, write the units, then choose the formula.

These are paper or simulator exercises. Physical work belongs in an appropriate supervised low-voltage lab, following the instructor's procedures. Do not experiment with mains electricity or unknown stored-energy components.

## 1. One resistor: check the prefixes

A `1 kOhm` resistor has `5 V` across it. For this ohmic model:

`I = V/R = 5/1000 = 0.005 A = 5 mA`

Its power dissipation is:

`P = VI = 5 * 0.005 = 0.025 W = 25 mW`

The common mistake is treating `1 kOhm` as `1 Ohm`. The result would be wrong by a factor of one thousand. Convert prefixes before substituting, or use a consistently understood scaled-unit method.

For an independent check, calculate `V^2/R`: `25/1000` gives the same `0.025 W`.

## 2. Series resistors: the current is shared

An ideal `12 V` source drives `2 kOhm` and `4 kOhm` in series. The equivalent resistance is `6 kOhm`, so:

`I = 12/6000 = 0.002 A = 2 mA`

The drops are `2 mA * 2 kOhm = 4 V` and `2 mA * 4 kOhm = 8 V`. Their sum is `12 V`, matching the source.

The larger resistance receives the larger drop because the branch current is the same. Do not decide that components are in series only because they are drawn side by side; check the connections.

## 3. Parallel branches: the voltage is shared

Put `3 kOhm` and `6 kOhm` across `12 V`. Each branch has that same voltage, giving currents of `4 mA` and `2 mA`. The total is `6 mA`.

The equivalent resistance is `12/0.006 = 2000 Ohm`. This is smaller than either positive branch resistance, which is a useful reasonableness check.

## Try before checking

1. What current flows through `2 kOhm` at `6 V`?
2. What is the equivalent of two `1 kOhm` resistors in parallel?
3. An unloaded divider has `3 kOhm` on top, `1 kOhm` on the bottom and an `8 V` input. What is the voltage across the bottom resistor?

Answers: `3 mA`, `500 Ohm` and `2 V`. For the divider, the result assumes that no extra load changes the bottom branch. State the model assumptions, not only the numerical result.

## More practice

The free [Computer Science Foundations book](/guides/computer-science-semester-one.pdf) includes a complete electrical-foundations chapter with original examples, 12 exercises and answers. Its [companion ZIP](/guides/computer-science-semester-one.zip) includes the editable notes and a balanced seven-module study pathway.

Further study: [MIT Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) and [OpenStax on electrical current](https://openstax.org/books/university-physics-volume-2/pages/9-1-electrical-current). These notes are independent study material, not an official lab manual.
