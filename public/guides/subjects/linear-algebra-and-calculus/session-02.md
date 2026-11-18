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
