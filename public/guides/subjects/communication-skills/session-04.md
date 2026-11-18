# Session 04 | Explaining a technical process

## What you should be able to do
Explain a process in a reproducible sequence with inputs and checks.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Explain the purpose before the mechanism. Introduce required terms, show the steps, then demonstrate with a small example. Distinguish what is always true from what holds only under stated assumptions. Use units, input ranges and expected outputs where relevant.

Worked example: To explain an average, first say it distributes the total equally across the count. Then show 10+20+30=60; divide by 3 to get 20. In C, explain that integer division discards the fractional part of a nonnegative result, so a real-valued average requires a floating-point operation. The concept and the language behavior are related but different ideas.

For instructions, start each step with an action and include a check: "Compile the file with the command shown. If compilation succeeds, run the executable. Confirm that the output is 20.00." Avoid "click there" without naming the control. A screenshot can support an instruction but should not be the only source of information.

## Reasoning in more depth
A process explanation should specify the starting state and the expected result. Use one action per step when sequencing matters. Tell the reader how to verify success and where an alternative path begins. Explain why a step exists if that reason prevents an error. Screenshots can support a procedure, but readable labels and text remain necessary when the interface differs or the image is inaccessible.

## Independent task | Attempt before reading the answer
Outline a procedure for compiling and running a small C program. Include prerequisites, success criteria and a troubleshooting branch.

## Worked answer and marking points
Prerequisites: a trusted local C compiler and a saved source file. In the source directory, compile with warnings enabled and choose an output name. If compilation fails, read the first diagnostic, correct the source and compile again. Run the produced executable and compare its output with the specified example. Compilation success checks translation; the output comparison checks one behavior. Neither alone proves all inputs are correct.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
