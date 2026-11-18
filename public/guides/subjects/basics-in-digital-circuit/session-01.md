# Session 01 | Number systems and representation

## What you should be able to do
Convert representations while stating width and signedness.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
In base b, a digit's place value is a power of b. Binary uses 0 and 1; hexadecimal uses 0-9 and A-F. Hexadecimal is convenient because one hex digit corresponds exactly to four bits. Leading zeroes do not change an unsigned value, but the chosen width matters for arithmetic and signed interpretation.

Worked example: 45 decimal = 32+8+4+1, so its six-bit binary form is 101101. Group into four-bit blocks with leading zeroes: 0010 1101, giving hex 2D. Checking back, 2*16+13=45.

To convert a fractional binary value, use negative powers of two. 0.101 binary = 1/2 + 0/4 + 1/8 = 0.625 decimal. Not every decimal fraction has a finite binary representation. The stored bit pattern and its interpretation must be specified; the same bits can represent an unsigned integer, a signed integer or part of another encoding.

## Reasoning in more depth
A bit pattern alone does not specify its meaning. The same pattern can encode an unsigned number, a signed number, a character or an instruction under different conventions. Positional binary uses powers of two. Hexadecimal groups four bits per digit, making long patterns easier to read without changing their value. Leading zeroes preserve an unsigned value but can matter when the width is part of a signed representation.

## Independent task | Attempt before reading the answer
Convert unsigned binary 101101 to decimal and hexadecimal. Then interpret 11111111 as unsigned and as 8-bit two's complement.

## Worked answer and marking points
101101=32+8+4+1=45 decimal and 2D hexadecimal (0010 1101). 11111111 is 255 unsigned. As an 8-bit two's-complement value it is -1. State the interpretation before assigning meaning to the pattern.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
