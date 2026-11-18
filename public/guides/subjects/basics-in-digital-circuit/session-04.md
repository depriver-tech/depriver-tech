# Session 04 | Boolean algebra and equivalent circuits

## What you should be able to do
Verify an algebraic simplification and apply De Morgan's law correctly.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Boolean algebra manipulates logic functions. Common laws include X+0=X, X*1=X, X+X=X, X*X=X, X+X'=1 and X*X'=0. Here + means OR, * means AND and ' means NOT; these symbols are not ordinary arithmetic in this context.

De Morgan's laws are (AB)'=A'+B' and (A+B)'=A'B'. They help convert between gate structures and reason about negated conditions. NAND and NOR are each functionally complete: suitable combinations can implement any Boolean function.

Worked example: Y=AB+AB'. Factor A to obtain A(B+B')=A*1=A. Four truth-table rows confirm that the output depends only on A. The simplified implementation needs only a connection carrying A, rather than redundant gates.

Be careful with distribution and negation. (A+B)' is not A'+B'. Write every complement over its intended expression, using parentheses in plain-text notes so the scope is unambiguous.

## Reasoning in more depth
Boolean algebra uses identities on binary values, so ordinary numeric intuition can mislead: A+A=A in OR notation. Apply De Morgan by complementing each term and exchanging AND with OR. Preserve parentheses until the scope of every complement is clear. You can verify a proposed simplification with a complete truth table for a small input count; one matching row is insufficient.

## Independent task | Attempt before reading the answer
Simplify Y=A OR (A AND B), and rewrite NOT(A OR B) using AND and complements.

## Worked answer and marking points
Absorption gives Y=A, since when A=1 the OR is already true and when A=0 both terms are false. De Morgan gives NOT A AND NOT B. The latter is true only for A=B=0. It is not the same as NOT A OR NOT B, which is false only when both inputs are 1.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
