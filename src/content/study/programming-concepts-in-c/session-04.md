---
title: "Loops, invariants and tracing"
module: "programming-concepts-in-c"
code: "CS 8138"
number: 4
objective: "Trace initialization, condition, body and update while maintaining an invariant."
---

## What you should be able to do
Trace initialization, condition, body and update while maintaining an invariant.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A for loop makes initialization, continuation condition and update visible together. A while loop checks its condition before every iteration; a do-while checks after the body. Choose the form that makes termination and state changes easiest to understand.

A loop invariant is a property that remains true at the relevant point in each iteration. For summing the first i array elements, the invariant can be: total equals the sum of elements with indices 0 through i-1. Initialize total to zero before the first iteration; add the next element; advance i. At i=n, the invariant yields the required whole-array sum.

Worked example: Sum the integers from 1 to 4. Before the loop, total=0. After i=1, total=1; after 2, total=3; after 3, total=6; after 4, total=10. Trace the actual update order rather than writing only the final answer. A condition i < 4 would omit the last term.

Watch for off-by-one errors, uninitialized accumulators, a condition that never changes, and updating the wrong variable. For very large data, also consider integer overflow and whether the chosen type is adequate.

## Reasoning in more depth
A loop invariant states a useful property that is true before and after each iteration. For summing an array, after i elements the sum should equal the total of the first i elements. Check initialization at i=0 and what one iteration adds. A termination argument shows that progress reaches the stopping condition. Consider the zero-iteration case and ensure the accumulator is initialized before it can be used.

## Independent task | Attempt before reading the answer
Trace sum=0; for (int i=1;i<=4;i++) sum+=i;. State the sum after each iteration and a useful invariant.

## Worked answer and marking points
The successive sums are 1,3,6,10. After processing i, sum=1+...+i. Before the first iteration the sum of no processed values is 0. Each step adds the next integer and i increases toward 5, when the condition fails. This small bound fits ordinary int; large inputs require overflow analysis.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
