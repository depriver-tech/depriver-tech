# Session 07 | Grammars and pushdown intuition

## What you should be able to do
Trace a context-free derivation and relate it to stack behavior.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A grammar generates strings using production rules. A context-free grammar has a single nonterminal on the left of each rule. Derivation repeatedly replaces a nonterminal using an available production. A parse tree records the structure of the derivation.

Worked example: S -> 0S1 | epsilon generates exactly 0^n1^n for n >= 0. To derive 0011: S -> 0S1 -> 00S11 -> 0011. Each use of 0S1 adds one zero at the front and one one at the back. The epsilon rule stops the expansion.

A pushdown automaton adds a stack, which provides a last-in, first-out form of unbounded memory. For 0^n1^n, push a marker for each 0 and pop one for each 1, enforcing the correct phase order. This explains why the language can be context-free even though it is not regular.

Ambiguity means that some string has more than one parse tree or appropriate derivation structure. A grammar for arithmetic may need precedence and associativity rules; recognizing valid tokens is not enough to determine the intended expression structure.

## Reasoning in more depth
The grammar S -> 0S1 | epsilon makes the matching dependency explicit: each recursive expansion adds a pair and the base case stops. A derivation is a sequence of rule applications; a parse tree shows nested structure. A pushdown strategy must reject a 0 after the 1 phase begins, even when total counts happen to match. Balanced counts alone do not enforce the required order.

## Independent task | Attempt before reading the answer
Derive 000111, then explain why 0101 is not generated even though it contains two zeroes and two ones.

## Worked answer and marking points
S -> 0S1 -> 00S11 -> 000S111 -> 000111. Every generated string places all zeroes before all ones because expansion nests around S. In 0101 a zero appears after a one; equal totals cannot overcome that ordering violation.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
