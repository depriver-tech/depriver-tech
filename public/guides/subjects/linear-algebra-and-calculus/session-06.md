# Session 06 | Derivatives measure local change

## What you should be able to do
Apply the product and chain rules and interpret derivative units.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
The derivative f'(a) is the limit of [f(a+h) - f(a)]/h as h -> 0, when the limit exists. It is the tangent slope and an instantaneous rate of change. The average slope over a finite interval is a different quantity.

Useful rules: d(x^n)/dx = n*x^(n-1); a constant differentiates to zero; the derivative of a sum is the sum of derivatives. The product rule is (uv)' = u'v + uv'. The quotient rule is (u/v)' = (u'v - uv')/v^2 where v != 0. The chain rule multiplies the outer derivative by the derivative of the inner expression.

Worked example: y = (3x + 1)^4. The outer derivative gives 4(3x + 1)^3, then the inner derivative contributes 3. Therefore y' = 12(3x + 1)^3. Missing the factor 3 is a common chain-rule error.

For s(t) = t^2 + 2t measured in metres, velocity is 2t + 2 metres per second and acceleration is 2 metres per second squared. Units help distinguish the quantities.

## Reasoning in more depth
A derivative is a rate per unit of the input. If position is metres and time is seconds, its derivative is metres per second. For a product of changing quantities, both factors contribute: (uv) prime=u prime*v+u*v prime. For a nested rule, multiply the outer rate by the inner rate. Writing the structure before calculating prevents the common mistake of differentiating only the outer expression.

## Independent task | Attempt before reading the answer
Differentiate y=(x^2+1)(3x-2) and z=(2x+1)^4. Evaluate both derivatives at x=1.

## Worked answer and marking points
y prime=2x(3x-2)+3(x^2+1), which equals 8 at x=1. z prime=4(2x+1)^3*2=8(2x+1)^3, which equals 216 at x=1. Expanding y first gives the same derivative and provides an independent check.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
