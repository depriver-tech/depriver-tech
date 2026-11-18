# MS 8121 | Linear Algebra and Calculus

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
By the end of this foundation module, you should be able to describe functions, solve small linear systems, interpret vectors and matrices, evaluate elementary limits, differentiate functions, and use integration to calculate accumulation. These are original foundation lessons based on the module title, not a reproduction of a lecturer's syllabus. Complete Sessions 1-8 in order; solve the practice questions before opening the answers.

Prerequisites: arithmetic with fractions, rearranging equations, powers, and basic coordinate geometry. If you cannot solve 3x + 4 = 19 or simplify x^2 / x for x != 0, revise algebra first.

## Session map
1. Functions are input-output rules
2. Vectors describe magnitude and direction
3. Matrices and transformations
4. Solving linear systems and understanding solutions
5. Limits and continuity
6. Derivatives measure local change
7. Optimization is a reasoning process
8. Integration measures accumulation

# Session 01 | Functions are input-output rules

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


# Session 02 | Vectors describe magnitude and direction

## What you should be able to do
Calculate components, length, dot products and a projection.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A vector can represent displacement, force or a list of features. In two dimensions, u = (u1, u2). Add component by component, and multiply each component by a scalar. The length is ||u|| = sqrt(u1^2 + u2^2). The dot product is u.v = u1v1 + u2v2. It also equals ||u|| ||v|| cos(theta), which connects arithmetic to angles. Two nonzero vectors are perpendicular when their dot product is zero.

Worked example: u = (3, 4), v = (4, -3). Their lengths are both 5. Their dot product is 12 - 12 = 0, so they are perpendicular. The unit vector in u's direction is (3/5, 4/5). Do not call u.v a vector: its result is a scalar.

In computing, vectors appear in graphics, optimization and data representations. These applications motivate the mathematics, but do not replace learning the operations by hand.

## Reasoning in more depth
The sign of a dot product tells you about alignment: positive means an acute angle, zero means perpendicular nonzero vectors, and negative means an obtuse angle. A projection isolates the part of one vector pointing along another: proj_v(u)=((u.v)/(v.v))v for nonzero v. The remaining component u-proj_v(u) is perpendicular to v. This is useful when separating a displacement into motion along a path and motion across it.

## Independent task | Attempt before reading the answer
Project u=(3,4) onto v=(1,0). Find the perpendicular remainder and verify its dot product with v.

## Worked answer and marking points
u.v=3 and v.v=1, so the projection is (3,0). The remainder is (0,4); (0,4).(1,0)=0. The original vector is the sum (3,0)+(0,4). Its length is 5, but the projection length is 3.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 03 | Matrices and transformations

## What you should be able to do
Check dimensions before multiplying and interpret a matrix as a transformation.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An m by n matrix has m rows and n columns. To add matrices, their dimensions must match. To multiply A of size m by n and B of size n by p, the inner dimensions n must match; AB then has size m by p. Each output entry is a row-column dot product. Matrix multiplication generally does not commute.

Worked example: A = [[1, 2], [0, 1]], B = [[2, 0], [3, 1]]. AB = [[8, 2], [3, 1]], while BA = [[2, 4], [3, 7]]. Different results are not an arithmetic error: applying transformations in a different order changes the transformation.

The identity I leaves compatible vectors unchanged. An inverse A^-1, when it exists, undoes A. For a 2 by 2 matrix [[a,b],[c,d]], det(A) = ad - bc. If the determinant is nonzero, A^-1 = (1/det(A)) [[d,-b],[-c,a]]. A zero determinant signals loss of independent information; a unique inverse does not exist.

## Reasoning in more depth
A matrix product can be valid in one order and invalid in the other. Even when both orders exist, the output sizes may differ. Multiplying by a column vector forms a weighted combination of the matrix columns. For a diagonal matrix, each coordinate scales independently; a zero diagonal entry collapses an axis, so an inverse cannot recover that coordinate. Check a proposed inverse by multiplication rather than trusting the appearance of its entries.

## Independent task | Attempt before reading the answer
Let A=[[2,0],[0,3]] and x=(4,-1). Compute Ax, det(A), and A inverse. Recover x from Ax.

## Worked answer and marking points
Ax=(8,-3). det(A)=6, so A inverse=[[1/2,0],[0,1/3]]. Applying it to (8,-3) gives (4,-1). Each coordinate is stretched independently and then divided by the corresponding nonzero scale.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


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


# Session 07 | Optimization is a reasoning process

## What you should be able to do
Compare critical points and boundaries in a constrained optimization problem.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
To optimize on a closed interval, identify the quantity to maximize or minimize, express it using one variable, identify the allowed interval, find interior critical points, and compare their values with endpoint values. A derivative of zero is a candidate, not automatic proof of a maximum.

Worked example: A rectangle has perimeter 20 m. Let one side be x, so the other is 10 - x, with 0 <= x <= 10 for the closed comparison. Area A(x) = 10x - x^2. Its derivative is 10 - 2x, giving x = 5. A(0) = A(10) = 0, A(5) = 25. The maximum is a 5 m by 5 m square of area 25 m^2.

In an exam, state the domain and give units. Do not optimize a formula without explaining what its variables represent.

## Reasoning in more depth
Setting a derivative to zero produces candidates, not an automatic maximum or minimum. On a closed interval, evaluate the function at endpoints and at interior points where its derivative is zero or undefined. Constraints matter: a mathematically interesting point outside the allowed interval cannot solve the stated problem. In an applied problem, define variables and units before taking a derivative.

## Independent task | Attempt before reading the answer
A rectangle has perimeter 20 m. Let one side be x. Write its area, state the physical domain and find the greatest area.

## Worked answer and marking points
The other side is 10-x, so A=x(10-x), with 0<x<10 for nondegenerate rectangles. A prime=10-2x gives x=5. The quadratic opens downward, so the maximum is 25 m^2 for a 5 m by 5 m square. At the limiting degenerate endpoints the area is zero.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 08 | Integration measures accumulation

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


## Practice set | Attempt independently
1. Find the real domain of h(x) = sqrt(5-x)/(x-2).
2. For u=(2,-1), v=(1,3), find u+v, 2u and u.v.
3. Find the length of (6,8) and a unit vector in its direction.
4. Multiply [[1,3],[2,0]] by the column vector (2,4).
5. Find the determinant and inverse of [[2,1],[1,1]].
6. Solve 2x+y=8 and x-y=1. Show an elimination step and check.
7. Explain the solution set of x+y=2 and 2x+2y=5.
8. Evaluate lim as x -> 3 of (x^2-9)/(x-3).
9. Differentiate x^3 - 4x + 7 and (x^2+1)^3.
10. For position s(t)=3t^2-t, find velocity at t=2 and acceleration.
11. Find the minimum of f(x)=x^2-6x+10 on [0,4].
12. Evaluate integral from 0 to 2 of (3x^2+2) dx and explain its units if x is seconds and the integrand is m/s.

## Answers and reasoning
1. The square root needs x <= 5; the denominator excludes x=2. Domain: (-infinity,2) union (2,5].
2. u+v=(3,2); 2u=(4,-2); u.v=2-3=-1.
3. Length 10. Divide each component by 10: (0.6,0.8).
4. First entry 1*2+3*4=14; second 2*2+0*4=4. Result (14,4).
5. Determinant 2*1-1*1=1. Inverse [[1,-1],[-1,2]]. Multiplying by the original gives I.
6. Add the equations: 3x=9, so x=3. Then y=2. Check 6+2=8 and 3-2=1.
7. Doubling the first equation gives 2x+2y=4, contradicting 5. No solution.
8. Cancel x-3 for x != 3 to obtain x+3. The limit is 6.
9. 3x^2-4; and, by the chain rule, 6x(x^2+1)^2.
10. v(t)=6t-1, so v(2)=11; acceleration a(t)=6. Use m/s and m/s^2 if s is metres and t is seconds.
11. f'(x)=2x-6 gives x=3. Endpoint values are f(0)=10 and f(4)=2; f(3)=1 is the minimum.
12. Antiderivative x^3+2x gives 8+4=12. The result is metres, representing displacement; the integrand is positive, so distance agrees.

## Check your understanding
Explain matrix multiplication without saying "multiply corresponding entries." Explain why a limit can exist where the function is undefined. Solve a new derivative and a new integral without looking at the rules. If you can only repeat these examples, choose different coefficients and try again.

Further study: MIT 18.06 Linear Algebra, https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/ ; OpenStax Calculus Volume 1, https://openstax.org/books/calculus-volume-1/pages/preface . These are independently published resources; the examples and exercises above were created for this pack.
