# Session 02 | Types, expressions and input

## What you should be able to do
Predict arithmetic conversions and validate an input before using it.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A variable has a type that constrains its representation and operations. int is suitable for many whole-number calculations; double represents floating-point values approximately; char represents a character-sized integer type. Exact widths and ranges depend on the implementation. Do not assume every integer is 32 bits. Use limits from the implementation when range matters.

Integer division is particularly important. If both operands are integers, 7/2 produces 3, not 3.5. Assigning the result to a double does not restore the discarded fraction. Use 7.0/2 or convert an operand before division. The remainder operator % applies to integer types. A zero divisor is invalid and must be handled before division.

Worked example: marks are 70, 71 and 72. Sum is 213, average is 71.0. To reveal an integer-division bug, choose a sum not divisible by the count: 70+71+73=214, and 214/3 as integers produces 71, while 214/3.0 gives about 71.3333. A good test distinguishes the incorrect and correct algorithms.

For interactive input, check whether conversion succeeds and whether the value is in the allowed range. The supplied marks example reads a line with fgets and checks integer conversion with strtol. Do not use gets; it cannot enforce the buffer size.

## Reasoning in more depth
The operand types decide integer division before assignment to a floating variable. Converting after division cannot recover the discarded fraction. Input conversion also needs a contract: distinguish a valid integer from trailing junk and reject values outside the supported range. Check return values rather than treating uninitialized or stale data as valid input. The supplied practice pack uses line-based parsing for robust examples.

## Independent task | Attempt before reading the answer
Predict double a=7/2 and double b=7/2.0. What does (double)(7/2) produce, and why?

## Worked answer and marking points
a becomes 3.0 because integer division produces 3 first. b becomes 3.5 because one operand is floating. (double)(7/2) also gives 3.0; the cast occurs after information has already been lost. Use (double)7/2 or 7/2.0 when a fractional quotient is required.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
