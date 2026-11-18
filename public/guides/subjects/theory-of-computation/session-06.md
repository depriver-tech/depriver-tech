# Session 06 | Why some languages need more memory

## What you should be able to do
Use the quantifier order of the pumping lemma correctly.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A finite automaton has a fixed amount of state memory, regardless of input length. Some tasks require keeping track of unbounded information. The language {0^n 1^n : n >= 0} requires matching the number of zeroes and ones, and is not regular.

The pumping lemma gives a necessary property of regular languages. If L is regular, there is a pumping length p such that every sufficiently long string s in L can be split s=xyz with |xy| <= p, |y| > 0 and xy^i z in L for all i >= 0. To prove nonregularity using it, assume regularity, choose a suitable string, and handle every permitted decomposition.

Worked example: Choose s=0^p1^p. Every valid y lies among the first p zeroes and contains at least one zero. Pumping down with i=0 removes zeroes but no ones, so the result is not in L. This contradicts the required property.

Do not use the lemma backwards: finding one pumpable string does not establish regularity. A regular-language construction, such as a DFA, is a more direct positive proof.

## Reasoning in more depth
The pumping length is supplied by the assumed regularity; you do not get to choose its numerical value. You choose a string after learning p, but an opponent may choose any decomposition satisfying the length restrictions. Your argument must defeat all of them using an allowed pumping exponent. A proof that only one convenient split fails leaves other splits available and therefore proves nothing about regularity.

## Independent task | Attempt before reading the answer
Explain why choosing y=0^p is unnecessary when proving {0^n1^n} nonregular. What is enough to know about y?

## Worked answer and marking points
For s=0^p1^p, every valid y is 0^k for some k>=1, since |xy|<=p. Pumping down removes k zeroes while retaining p ones. The counts differ for every possible k, so the proof works without selecting a specific decomposition.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
