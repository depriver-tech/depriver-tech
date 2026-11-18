---
title: "Functions, scope and contracts"
module: "programming-concepts-in-c"
code: "CS 8138"
number: 5
objective: "Specify a function contract and distinguish local changes from caller state."
---

## What you should be able to do
Specify a function contract and distinguish local changes from caller state.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A function packages a coherent operation. Its declaration communicates parameter types and return type. Its contract states what callers must provide and what the function promises. C passes argument values; modifying a parameter variable does not modify the caller's separate variable.

Worked example: int square(int x) returns x*x for values whose square is representable as int. The range qualification matters: a mathematically valid square can overflow the chosen integer type. A function that sums a fixed small array can have a straightforward contract; a production function may need explicit overflow handling.

Prefer one responsibility per function. Separate reading input from calculating a result when this makes testing easier. A calculation function can then be checked with known inputs without simulating a keyboard.

Local variables normally exist within their block's scope. Do not return the address of an automatic local variable; its lifetime ends when the function returns. Use meaningful names such as count, capacity and total instead of assigning every variable a single letter.

## Reasoning in more depth
A function contract describes valid inputs, promised output and any side effects. Parameter values in C are passed by value. Changing a scalar parameter changes the local copy, while dereferencing a valid pointer can change an object owned elsewhere. Do not return a pointer to a local automatic object whose lifetime ends at return. Separating calculation from input/output makes functions easier to test.

## Independent task | Attempt before reading the answer
For int square(int x){return x*x;}, state the arithmetic precondition. Does calling square(a) change a?

## Worked answer and marking points
The product must be representable in int; otherwise signed overflow gives undefined behavior. A contract should restrict x accordingly or use checked arithmetic. Calling square(a) does not modify a because x is a local value copy. Save the result explicitly if needed. A wider return type alone does not widen the multiplication unless the operands are converted before multiplying.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
