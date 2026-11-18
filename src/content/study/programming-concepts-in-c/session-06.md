---
title: "Arrays, strings and bounds"
module: "programming-concepts-in-c"
code: "CS 8138"
number: 6
objective: "Keep array accesses within bounds and account for a string terminator."
---

## What you should be able to do
Keep array accesses within bounds and account for a string terminator.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An array holds a fixed number of elements of the same type. For n elements, valid indices are 0 through n-1. C does not automatically check ordinary array subscripts. Accessing outside the array is not a reliable way to obtain a convenient value; it is a program error with potentially undefined behavior.

A C string is a sequence of characters terminated by a zero byte, '\0'. A buffer must have space for both the visible characters and this terminator. The newline character '\n' is different from the string terminator. A character literal uses single quotes; a string literal uses double quotes.

Worked example: char word[4] = "cat" contains 'c', 'a', 't', '\0'. It has capacity 4 but visible string length 3. Storing four visible letters as a string would require at least five elements. The sizeof operator measures the array object in bytes where its type is still an array; strlen counts visible characters before the terminator.

When arrays are passed to ordinary function parameters, the parameter does not retain the array length automatically. Pass a count or another explicit bound. The supplied array program demonstrates an index loop and a separate count.

## Reasoning in more depth
An array of n elements has valid indices 0 through n-1. A pointer to the first element does not carry the length, so pass the length separately where needed. A C string requires a terminating null byte within its valid storage. The size of an array object and the length of its current string are different quantities. Bounds errors can corrupt unrelated state and cannot be diagnosed reliably from apparently correct output.

## Independent task | Attempt before reading the answer
For char name[5]="MUST";, give sizeof(name), the string length and the highest valid index. Can it hold "STUDY" as a C string?

## Worked answer and marking points
The array has five char slots, sizeof(name)=5, string length=4 and highest valid index=4. Index 4 stores the null terminator. STUDY has five visible characters and needs six slots including the terminator, so it cannot fit as a C string in this array.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
