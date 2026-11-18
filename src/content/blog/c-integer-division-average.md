---
title: "Why your C average is wrong: integer division, explained with a working example"
description: "A small C bug with a big lesson: why assigning to double does not repair integer division, how to fix the expression, and which tests reveal the mistake."
date: 2026-11-18
status: live
tags: ["students", "programming", "debugging"]
---

A program can compile, run and still produce the wrong answer. Integer division is a good example because the mistake can look reasonable on screen.

*Usikariri formula tu. Angalia aina za data na matokeo ya kila hatua.* Do not only memorize the formula; follow the types and the intermediate result.

## The bug

Suppose three marks are 70, 71 and 73. Their total is 214. The mathematical average is 214/3, approximately 71.3333.

```c
int total = 214;
int count = 3;
double average = total / count;
```

This stores 71.0, not 71.3333. Both operands of `/` are integers, so C performs integer division first. Only afterwards does assignment convert the result to `double`. The fraction is already gone.

## Convert before dividing

```c
double average = (double)total / count;
```

Converting one operand makes the division a floating-point operation. For this small example, the result is the expected approximation. In a general program, also check that the count is nonzero and that accumulating the total cannot overflow its type.

Here is a complete standard-library example:

```c
#include <stdio.h>

int main(void) {
    const int marks[] = {70, 71, 73};
    const size_t count = sizeof marks / sizeof marks[0];
    int total = 0;
    for (size_t i = 0; i < count; ++i) {
        total += marks[i];
    }
    printf("Average: %.2f\n", (double)total / (double)count);
    return 0;
}
```

Compile with `clang -std=c17 -Wall -Wextra -Wpedantic average.c -o average`, then run `./average`. Expected output: `Average: 71.33`. Formatting to two decimal places changes the displayed precision; it does not fix the original integer-division bug.

## Choose a test that can expose the error

If the marks total 210, then both the wrong integer expression and the corrected expression display 70.00. That test cannot distinguish them. A total such as 214 is useful because it is not divisible by 3.

Try predicting the results of `9/4`, `9%4` and `9/4.0` before running them. The answers are 2, 1 and 2.25. Then explain why each expression has that result.

The transferable lesson is to trace the operation before the assignment. Ask: what are the operand types, what operation happens now, and what information has already been lost?

## Practise with the new semester-one study pack

The free [Computer Science Foundations book](/guides/computer-science-semester-one.pdf) covers seven first-semester foundation modules. Its [companion ZIP](/guides/computer-science-semester-one.zip) includes editable notes, six C programs and a test runner. All 15 supplied execution tests passed when the pack was prepared.

The notes are independent learning material, not official university courseware or a substitute for your lecturer's current outline.

Further reading: [Harvard CS50 C materials](https://cs50.harvard.edu/x/weeks/1/) and the [WG14 N1570 language reference](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), a C11-era draft useful for these shared foundations.
