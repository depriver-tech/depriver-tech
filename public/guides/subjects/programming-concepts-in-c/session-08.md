# Session 08 | Files, testing and debugging

## What you should be able to do
Test file operations and debug by comparing predictions with observations.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A file operation can fail. Check fopen before using its result, check read/write outcomes where relevant, and close an opened stream. Choose the mode intentionally: opening a file with "w" can truncate an existing file. The supplied file example writes only in a newly created test directory.

Worked example: To write three marks, open a practice file, write each mark on a separate line, check success, close the file, reopen for reading and verify the sum. The program should report failure rather than pretending success when the file cannot be opened. Never point a practice program at an important file.

Test valid, boundary and invalid cases. A mark parser should consider 0,100,-1,101, a nonnumeric string and a numeric string with unwanted trailing characters. For an average, use a total that is not evenly divisible by the count. Explain what each case is intended to expose.

Debug systematically: reproduce the failure, reduce the example, inspect warnings, trace state, change one cause, and rerun both the failing case and earlier passing cases. A program that compiles is not necessarily correct. Sanitizers can help find memory errors when supported; they do not prove correctness.

## Reasoning in more depth
Check that opening a file succeeded before reading or writing it. Check relevant operation results, then close the resource. A test should state its input, expected output and why that case matters. Test missing files, empty input and boundaries alongside the normal path. Debugging begins with the earliest point where observed state differs from the intended invariant, not with random edits until one run appears correct.

## Independent task | Attempt before reading the answer
Design four tests for a program that reads marks and reports their mean. State the intended behavior for an empty input.

## Worked answer and marking points
Tests: one mark 50 -> mean 50; marks 0 and 100 -> mean 50; marks 1 and 2 -> mean 1.5 to expose integer division; an empty file -> a clear no-data outcome without division by zero. Also test malformed and out-of-range input under the chosen rejection contract. Expected results must be written before running the program.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
