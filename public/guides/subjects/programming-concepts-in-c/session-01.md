# Session 01 | From problem to executable

## What you should be able to do
Connect a problem specification to translation and a verified run.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An algorithm is a precise sequence of steps that transforms allowed inputs into required outputs. Before coding, state the inputs, output, constraints and exceptional cases. Pseudocode helps separate the logic from language syntax.

A C source file is translated and linked into an executable. Compilation errors differ from runtime failures and wrong answers. Use warnings to expose suspicious code early. In the practice folder, compile with a command such as:

```sh
clang -std=c17 -Wall -Wextra -Wpedantic average.c -o average
./average
```

Worked example: To find the maximum of three numbers, start with the first as the current maximum; compare the second and update if larger; repeat for the third. Starting at zero would fail if all inputs were negative. A correct initial value should follow from the problem, not from habit.

A minimal program uses #include <stdio.h>, an int main(void) function, statements within braces, and a return value. A semicolon terminates many statements; braces group a block. Keep indentation consistent so the structure can be inspected.

## Reasoning in more depth
Start with inputs, outputs and boundary behavior before choosing syntax. Translation can succeed even when the program implements the wrong requirement. A compiler diagnostic may identify where a contradiction becomes visible rather than the earliest source of the error. Fix the first useful diagnostic, rebuild and rerun the selected examples. Keep the source file distinct from the executable so a stale executable cannot disguise a failed build.

## Independent task | Attempt before reading the answer
Specify a program that converts whole minutes into hours and remaining minutes. Give normal and boundary examples before coding.

## Worked answer and marking points
For nonnegative whole input m, hours=m/60 and remainder=m%60. Examples: 0 -> 0 h 0 min; 59 -> 0 h 59 min; 60 -> 1 h 0 min; 125 -> 2 h 5 min. State whether invalid, negative or out-of-range input is rejected. The remainder should satisfy 0<=remainder<60.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
