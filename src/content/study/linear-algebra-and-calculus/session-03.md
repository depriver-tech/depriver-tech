---
title: "Matrices and transformations"
module: "linear-algebra-and-calculus"
code: "MS 8121"
number: 3
objective: "Check dimensions before multiplying and interpret a matrix as a transformation."
---

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
