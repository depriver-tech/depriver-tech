# Session 05 | Limits and continuity

## What you should be able to do
Use one-sided limits to check whether a removable or jump discontinuity occurs.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A limit describes what outputs approach as inputs approach a value; it does not require the function to be defined at that value. Direct substitution works for many continuous expressions. A 0/0 result is an indeterminate form: simplify or use another valid method rather than declaring the limit zero.

Worked example: lim as x -> 2 of (x^2 - 4)/(x - 2). Factor the numerator: (x - 2)(x + 2). For x != 2 the quotient equals x + 2, so the limit is 4. The original expression remains undefined at 2. Defining its value there as 4 would remove the discontinuity.

A function is continuous at a when f(a) exists, the two-sided limit exists, and that limit equals f(a). Left and right limits must agree. For f(x) = |x|/x, the left limit at zero is -1 and the right limit is 1, so the two-sided limit does not exist.

## Reasoning in more depth
A two-sided limit is a statement that both directions approach the same finite value. A table of nearby values suggests a result but does not prove it; algebra or a valid theorem supplies the reason. At a removable hole, the limiting value exists and can define a continuous extension. At a jump, assigning one value at the point cannot make unequal one-sided limits agree.

## Independent task | Attempt before reading the answer
For f(x)=(x^2-9)/(x-3), x!=3, find the limit at 3 and the value needed for continuity. Compare with h(x)=0 for x<3 and h(x)=1 for x>=3.

## Worked answer and marking points
Factor f to x+3 for x!=3. Its limit is 6, so defining f(3)=6 removes the hole. For h, the left limit is 0 and the right limit is 1. The two-sided limit fails and changing h(3) alone cannot make it continuous.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
