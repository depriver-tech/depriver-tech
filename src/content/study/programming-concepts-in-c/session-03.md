---
title: "Selection and Boolean conditions"
module: "programming-concepts-in-c"
code: "CS 8138"
number: 3
objective: "Construct boundary conditions with the correct logical operators."
---

## What you should be able to do
Construct boundary conditions with the correct logical operators.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An if statement chooses a branch when its condition is nonzero. A comparison such as x == 0 tests equality; x = 0 assigns a value. Logical AND is &&, logical OR is ||, and logical NOT is !. These differ from the bitwise operators &, | and ~.

Worked example: A valid mark must satisfy mark >= 0 && mark <= 100. Writing 0 <= mark <= 100 does not express a mathematical chained inequality in C. The first comparison yields 0 or 1, and the second comparison then compares that result with 100. Write both comparisons explicitly.

Check ranges in a sensible order. For classification, validate the input first, then apply the categories. Avoid using overlapping independent if statements when exactly one category should be chosen. An if / else if / else chain expresses mutual choice.

Short-circuit behavior matters. In divisor != 0 && total/divisor > 2, the division is not evaluated when divisor is zero. This is useful, but the condition must still match the intended logic. Never rely on unspecified evaluation order of unrelated expressions.

## Reasoning in more depth
Translate a requirement into a Boolean sentence before writing an if statement. An inclusive interval requires both bounds, so use logical AND. Being outside the interval requires at least one failure, so use OR. Test a value below the interval, each endpoint, an interior value and a value above it. In C, assignment and comparison use different operators, and chained mathematical comparisons do not express an interval correctly.

## Independent task | Attempt before reading the answer
Write conditions for an integer mark in [0,100] and outside it. Explain why 0<=mark<=100 is wrong in C.

## Worked answer and marking points
Valid: mark>=0 && mark<=100. Invalid: mark<0 || mark>100. In C, 0<=mark is evaluated first as 0 or 1; that result is then compared with 100, so the chained expression does not test the intended range. Test -1,0,50,100,101.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
