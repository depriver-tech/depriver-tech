# MS 8121 | Linear Algebra and Calculus

## Learning outcomes and route
By the end of this foundation module, you should be able to describe functions, solve small linear systems, interpret vectors and matrices, evaluate elementary limits, differentiate functions, and use integration to calculate accumulation. These are original foundation lessons based on the module title, not a reproduction of a lecturer's syllabus. Complete Lessons 1-8 in order; solve the practice questions before opening the answers.

Prerequisites: arithmetic with fractions, rearranging equations, powers, and basic coordinate geometry. If you cannot solve 3x + 4 = 19 or simplify x^2 / x for x != 0, revise algebra first.

## Lesson 1 | Functions are input-output rules
A function assigns exactly one output to each allowed input. The domain is the set of allowed inputs; the range is the set of outputs actually reached. Writing f(x) does not mean f multiplied by x. It names the output of f at x. A graph is a collection of input-output pairs, not simply a picture to memorize.

For a quotient, exclude values making the denominator zero. For a real square root, the quantity inside must be nonnegative. Composition means applying one rule after another: (f o g)(x) = f(g(x)). The order usually matters. An inverse reverses a one-to-one rule on a suitable domain; the reciprocal 1/f(x) generally does not.

Worked example: Let f(x) = sqrt(x - 2), g(x) = x + 5. The domain of f is x >= 2. The composition f(g(x)) = sqrt(x + 3) has domain x >= -3. Meanwhile g(f(x)) = sqrt(x - 2) + 5 still requires x >= 2. Checking the domain is part of the answer.

Try explaining to a friend why a function can have several inputs giving the same output, but cannot assign two different outputs to the same input.

## Lesson 2 | Vectors describe magnitude and direction
A vector can represent displacement, force or a list of features. In two dimensions, u = (u1, u2). Add component by component, and multiply each component by a scalar. The length is ||u|| = sqrt(u1^2 + u2^2). The dot product is u.v = u1v1 + u2v2. It also equals ||u|| ||v|| cos(theta), which connects arithmetic to angles. Two nonzero vectors are perpendicular when their dot product is zero.

Worked example: u = (3, 4), v = (4, -3). Their lengths are both 5. Their dot product is 12 - 12 = 0, so they are perpendicular. The unit vector in u's direction is (3/5, 4/5). Do not call u.v a vector: its result is a scalar.

In computing, vectors appear in graphics, optimization and data representations. These applications motivate the mathematics, but do not replace learning the operations by hand.

## Lesson 3 | Matrices and transformations
An m by n matrix has m rows and n columns. To add matrices, their dimensions must match. To multiply A of size m by n and B of size n by p, the inner dimensions n must match; AB then has size m by p. Each output entry is a row-column dot product. Matrix multiplication generally does not commute.

Worked example: A = [[1, 2], [0, 1]], B = [[2, 0], [3, 1]]. AB = [[8, 2], [3, 1]], while BA = [[2, 4], [3, 7]]. Different results are not an arithmetic error: applying transformations in a different order changes the transformation.

The identity I leaves compatible vectors unchanged. An inverse A^-1, when it exists, undoes A. For a 2 by 2 matrix [[a,b],[c,d]], det(A) = ad - bc. If the determinant is nonzero, A^-1 = (1/det(A)) [[d,-b],[-c,a]]. A zero determinant signals loss of independent information; a unique inverse does not exist.

## Lesson 4 | Solving linear systems and understanding solutions
Write a system as an augmented matrix [A | b]. Elementary row operations swap rows, multiply a row by a nonzero number, or add a multiple of one row to another. They preserve the solution set. Eliminate variables, find pivots, then back-substitute. A row [0 0 | nonzero] is a contradiction. A free variable can give infinitely many solutions when the system is consistent.

Worked example: x + 2y = 7 and 3x + y = 11. Subtract three times the first equation from the second: -5y = -10, so y = 2 and x = 3. Substituting into both original equations checks the result: 3 + 4 = 7; 9 + 2 = 11.

Linear independence means that the only coefficients producing the zero vector are all zero. The vectors (1,2) and (2,4) are dependent because the second is twice the first. They do not provide two independent directions. Rank counts independent rows or columns. This helps explain why some systems do not identify a unique answer.

## Lesson 5 | Limits and continuity
A limit describes what outputs approach as inputs approach a value; it does not require the function to be defined at that value. Direct substitution works for many continuous expressions. A 0/0 result is an indeterminate form: simplify or use another valid method rather than declaring the limit zero.

Worked example: lim as x -> 2 of (x^2 - 4)/(x - 2). Factor the numerator: (x - 2)(x + 2). For x != 2 the quotient equals x + 2, so the limit is 4. The original expression remains undefined at 2. Defining its value there as 4 would remove the discontinuity.

A function is continuous at a when f(a) exists, the two-sided limit exists, and that limit equals f(a). Left and right limits must agree. For f(x) = |x|/x, the left limit at zero is -1 and the right limit is 1, so the two-sided limit does not exist.

## Lesson 6 | Derivatives measure local change
The derivative f'(a) is the limit of [f(a+h) - f(a)]/h as h -> 0, when the limit exists. It is the tangent slope and an instantaneous rate of change. The average slope over a finite interval is a different quantity.

Useful rules: d(x^n)/dx = n*x^(n-1); a constant differentiates to zero; the derivative of a sum is the sum of derivatives. The product rule is (uv)' = u'v + uv'. The quotient rule is (u/v)' = (u'v - uv')/v^2 where v != 0. The chain rule multiplies the outer derivative by the derivative of the inner expression.

Worked example: y = (3x + 1)^4. The outer derivative gives 4(3x + 1)^3, then the inner derivative contributes 3. Therefore y' = 12(3x + 1)^3. Missing the factor 3 is a common chain-rule error.

For s(t) = t^2 + 2t measured in metres, velocity is 2t + 2 metres per second and acceleration is 2 metres per second squared. Units help distinguish the quantities.

## Lesson 7 | Optimization is a reasoning process
To optimize on a closed interval, identify the quantity to maximize or minimize, express it using one variable, identify the allowed interval, find interior critical points, and compare their values with endpoint values. A derivative of zero is a candidate, not automatic proof of a maximum.

Worked example: A rectangle has perimeter 20 m. Let one side be x, so the other is 10 - x, with 0 <= x <= 10 for the closed comparison. Area A(x) = 10x - x^2. Its derivative is 10 - 2x, giving x = 5. A(0) = A(10) = 0, A(5) = 25. The maximum is a 5 m by 5 m square of area 25 m^2.

In an exam, state the domain and give units. Do not optimize a formula without explaining what its variables represent.

## Lesson 8 | Integration measures accumulation
An indefinite integral describes a family of antiderivatives, so include + C. For n != -1, integral x^n dx = x^(n+1)/(n+1) + C. The special case integral 1/x dx is ln|x| + C on intervals avoiding zero. Substitution reverses the chain rule.

A definite integral gives signed accumulation over an interval. If F' = f and the usual continuity conditions hold, integral from a to b of f(x) dx = F(b) - F(a). Areas below the horizontal axis contribute negatively; total geometric area may require splitting the interval and changing signs.

Worked example: A velocity v(t) = 2t + 1 m/s over 0 <= t <= 3 gives displacement [t^2 + t] from 0 to 3 = 12 m. Since v is positive throughout, distance is also 12 m. With a sign-changing velocity, displacement and distance can differ.

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
