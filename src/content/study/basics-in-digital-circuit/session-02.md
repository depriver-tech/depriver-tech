---
title: "Binary arithmetic and two's complement"
module: "basics-in-digital-circuit"
code: "CS 8102"
number: 2
objective: "Perform fixed-width addition and distinguish carry from signed overflow."
---

## What you should be able to do
Perform fixed-width addition and distinguish carry from signed overflow.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Binary addition follows carry rules: 1+1 gives sum bit 0 and carry 1. For an n-bit unsigned value, the representable range is 0 through 2^n-1. An n-bit two's-complement value represents -2^(n-1) through 2^(n-1)-1. Interpret the most significant bit with negative weight when reading two's complement.

Worked example: In 8-bit two's complement, -5 is found by inverting 00000101 to 11111010 and adding 1, giving 11111011. Adding this to 00001001 (9) gives 1 00000100. Discarding the carry beyond 8 bits yields 00000100, which is 4.

Carry-out and signed overflow are different concepts. Adding 01111111 and 00000001 gives 10000000 in 8 bits: an unsigned result of 128 fits, but the signed mathematical result 128 is outside the two's-complement range, so signed overflow occurred. Always state width and interpretation before judging overflow.

## Reasoning in more depth
Unsigned overflow concerns a carry beyond the chosen width. Signed two's-complement overflow concerns a mathematical answer outside the signed range. Adding two positive operands and obtaining a negative sign indicates signed overflow; a final carry is not the signed-overflow criterion. Hardware can expose flags, while a programming language may assign different semantics to overflow, so do not transfer a circuit model into C without checking the language rules.

## Independent task | Attempt before reading the answer
Add 0111 and 0001 using four bits. Interpret the result as unsigned and signed two's complement.

## Worked answer and marking points
The four-bit result is 1000. Unsigned, 7+1=8 and no carry beyond four bits occurs. Signed four-bit values range -8 to 7, so +8 is unrepresentable; the pattern reads -8 and signed overflow occurred. The same bit addition has different conclusions under the two interpretations.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
