---
title: "Functions are input-output rules"
module: "linear-algebra-and-calculus"
code: "MS 8121"
number: 1
objective: "Determine domains and distinguish composition from inversion."
---

## What you should be able to do
Determine domains and distinguish composition from inversion.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A function assigns exactly one output to each allowed input. The domain is the set of allowed inputs; the range is the set of outputs actually reached. Writing f(x) does not mean f multiplied by x. It names the output of f at x. A graph is a collection of input-output pairs, not simply a picture to memorize.

For a quotient, exclude values making the denominator zero. For a real square root, the quantity inside must be nonnegative. Composition means applying one rule after another: (f o g)(x) = f(g(x)). The order usually matters. An inverse reverses a one-to-one rule on a suitable domain; the reciprocal 1/f(x) generally does not.

Worked example: Let f(x) = sqrt(x - 2), g(x) = x + 5. The domain of f is x >= 2. The composition f(g(x)) = sqrt(x + 3) has domain x >= -3. Meanwhile g(f(x)) = sqrt(x - 2) + 5 still requires x >= 2. Checking the domain is part of the answer.

Try explaining to a friend why a function can have several inputs giving the same output, but cannot assign two different outputs to the same input.

## Reasoning in more depth
A domain restriction follows the operations actually performed. Simplifying an expression can conceal a forbidden input: (x^2-1)/(x-1) agrees with x+1 only where x is not 1. When composing functions, check both the inner expression and whether its output is allowed by the outer function. To find an inverse, write y=f(x), solve for x, then exchange the variable names and check the resulting domain. Squaring loses sign information unless the starting domain is restricted.

## Independent task | Attempt before reading the answer
Let f(x)=2x-3 and g(x)=1/x. Find f(g(x)), g(f(x)) and f inverse. Give all domains.

## Worked answer and marking points
f(g(x))=2/x-3 requires x!=0. g(f(x))=1/(2x-3) requires x!=3/2. From y=2x-3, x=(y+3)/2, so f inverse(x)=(x+3)/2 for every real x. The two compositions are different rules with different excluded inputs.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
