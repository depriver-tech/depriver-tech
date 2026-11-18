# Session 04 | Solving linear systems and understanding solutions

## What you should be able to do
Classify a system as having one, none or infinitely many solutions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Write a system as an augmented matrix [A | b]. Elementary row operations swap rows, multiply a row by a nonzero number, or add a multiple of one row to another. They preserve the solution set. Eliminate variables, find pivots, then back-substitute. A row [0 0 | nonzero] is a contradiction. A free variable can give infinitely many solutions when the system is consistent.

Worked example: x + 2y = 7 and 3x + y = 11. Subtract three times the first equation from the second: -5y = -10, so y = 2 and x = 3. Substituting into both original equations checks the result: 3 + 4 = 7; 9 + 2 = 11.

Linear independence means that the only coefficients producing the zero vector are all zero. The vectors (1,2) and (2,4) are dependent because the second is twice the first. They do not provide two independent directions. Rank counts independent rows or columns. This helps explain why some systems do not identify a unique answer.

## Reasoning in more depth
Row reduction preserves equations because each permitted operation is reversible. A pivot identifies a constrained variable. If a consistent two-variable system has only one independent equation, choosing one variable determines the other, giving a family rather than a single answer. Write that family with a parameter and substitute it back. A contradiction row means no choice of the parameter can repair the system.

## Independent task | Attempt before reading the answer
Classify x+2y=5, 2x+4y=10 and describe every solution. What changes if the second right-hand side is 11?

## Worked answer and marking points
Subtract twice the first row from the second. With right-hand side 10, the result is 0=0. Let y=t and x=5-2t for any real t. With right-hand side 11 the result is 0=1, a contradiction, so no solutions exist.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
