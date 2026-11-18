---
title: "Integration measures accumulation"
module: "linear-algebra-and-calculus"
code: "MS 8121"
number: 8
objective: "Calculate signed accumulation and distinguish displacement from distance."
---

## What you should be able to do
Calculate signed accumulation and distinguish displacement from distance.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An indefinite integral describes a family of antiderivatives, so include + C. For n != -1, integral x^n dx = x^(n+1)/(n+1) + C. The special case integral 1/x dx is ln|x| + C on intervals avoiding zero. Substitution reverses the chain rule.

A definite integral gives signed accumulation over an interval. If F' = f and the usual continuity conditions hold, integral from a to b of f(x) dx = F(b) - F(a). Areas below the horizontal axis contribute negatively; total geometric area may require splitting the interval and changing signs.

Worked example: A velocity v(t) = 2t + 1 m/s over 0 <= t <= 3 gives displacement [t^2 + t] from 0 to 3 = 12 m. Since v is positive throughout, distance is also 12 m. With a sign-changing velocity, displacement and distance can differ.

## Reasoning in more depth
A definite integral adds signed contributions. Negative velocity decreases displacement but still contributes positive travel distance. Split an interval where the velocity changes sign before adding absolute contributions for distance. An antiderivative needs a constant for an indefinite integral; the constant cancels when evaluating a definite integral by upper-minus-lower substitution.

## Independent task | Attempt before reading the answer
A velocity is v(t)=2t-2 m/s for 0<=t<=2 s. Find displacement and total distance.

## Worked answer and marking points
An antiderivative is t^2-2t. Displacement is its value at 2 minus its value at 0, or 0 m. Velocity changes sign at t=1. The displacement on [0,1] is -1 m and on [1,2] is +1 m, so total distance is 2 m.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
