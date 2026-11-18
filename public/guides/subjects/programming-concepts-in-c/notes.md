# CS 8138 | Programming Concepts in C

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
Learn to turn a problem into a precise algorithm, express it in C, compile with warnings, test boundary cases and explain the result. This foundation course covers types, control flow, functions, arrays, strings, pointers, structures, files and debugging. The supplied practice folder contains standalone C17 programs and a test runner. They use the standard library, not a course-specific library.

Prerequisites: basic arithmetic and a willingness to trace variables on paper. Start with small correct programs; do not begin with a large menu system whose parts you cannot explain.

## Session map
1. From problem to executable
2. Types, expressions and input
3. Selection and Boolean conditions
4. Loops, invariants and tracing
5. Functions, scope and contracts
6. Arrays, strings and bounds
7. Pointers, structures and data ownership
8. Files, testing and debugging

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


# Session 03 | Selection and Boolean conditions

## What you should be able to do
Construct boundary conditions with the correct logical operators.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An if statement chooses a branch when its condition is nonzero. A comparison such as x == 0 tests equality; x = 0 assigns a value. Logical AND is &&, logical OR is ||, and logical NOT is !. These differ from the bitwise operators &, | and ~.

Worked example: A valid mark must satisfy mark >= 0 && mark <= 100. Writing 0 <= mark <= 100 does not express a mathematical chained inequality in C. The first comparison yields 0 or 1, and the second comparison then compares that result with 100. Write both comparisons explicitly.

Check ranges in a sensible order. For classification, validate the input first, then apply the categories. Avoid using overlapping independent if statements when exactly one category should be chosen. An if / else if / else chain expresses mutual choice.

Short-circuit behavior matters. In divisor != 0 && total/divisor > 2, the division is not evaluated when divisor is zero. This is useful, but the condition must still match the intended logic. Never rely on unspecified evaluation order of unrelated expressions.

## Reasoning in more depth
Translate a requirement into a Boolean sentence before writing an if statement. An inclusive interval requires both bounds, so use logical AND. Being outside the interval requires at least one failure, so use OR. Test a value below the interval, each endpoint, an interior value and a value above it. In C, assignment and comparison use different operators, and chained mathematical comparisons do not express an interval correctly.

## Independent task | Attempt before reading the answer
Write conditions for an integer mark in [0,100] and outside it. Explain why 0<=mark<=100 is wrong in C.

## Worked answer and marking points
Valid: mark>=0 && mark<=100. Invalid: mark<0 || mark>100. In C, 0<=mark is evaluated first as 0 or 1; that result is then compared with 100, so the chained expression does not test the intended range. Test -1,0,50,100,101.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 04 | Loops, invariants and tracing

## What you should be able to do
Trace initialization, condition, body and update while maintaining an invariant.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A for loop makes initialization, continuation condition and update visible together. A while loop checks its condition before every iteration; a do-while checks after the body. Choose the form that makes termination and state changes easiest to understand.

A loop invariant is a property that remains true at the relevant point in each iteration. For summing the first i array elements, the invariant can be: total equals the sum of elements with indices 0 through i-1. Initialize total to zero before the first iteration; add the next element; advance i. At i=n, the invariant yields the required whole-array sum.

Worked example: Sum the integers from 1 to 4. Before the loop, total=0. After i=1, total=1; after 2, total=3; after 3, total=6; after 4, total=10. Trace the actual update order rather than writing only the final answer. A condition i < 4 would omit the last term.

Watch for off-by-one errors, uninitialized accumulators, a condition that never changes, and updating the wrong variable. For very large data, also consider integer overflow and whether the chosen type is adequate.

## Reasoning in more depth
A loop invariant states a useful property that is true before and after each iteration. For summing an array, after i elements the sum should equal the total of the first i elements. Check initialization at i=0 and what one iteration adds. A termination argument shows that progress reaches the stopping condition. Consider the zero-iteration case and ensure the accumulator is initialized before it can be used.

## Independent task | Attempt before reading the answer
Trace sum=0; for (int i=1;i<=4;i++) sum+=i;. State the sum after each iteration and a useful invariant.

## Worked answer and marking points
The successive sums are 1,3,6,10. After processing i, sum=1+...+i. Before the first iteration the sum of no processed values is 0. Each step adds the next integer and i increases toward 5, when the condition fails. This small bound fits ordinary int; large inputs require overflow analysis.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 05 | Functions, scope and contracts

## What you should be able to do
Specify a function contract and distinguish local changes from caller state.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A function packages a coherent operation. Its declaration communicates parameter types and return type. Its contract states what callers must provide and what the function promises. C passes argument values; modifying a parameter variable does not modify the caller's separate variable.

Worked example: int square(int x) returns x*x for values whose square is representable as int. The range qualification matters: a mathematically valid square can overflow the chosen integer type. A function that sums a fixed small array can have a straightforward contract; a production function may need explicit overflow handling.

Prefer one responsibility per function. Separate reading input from calculating a result when this makes testing easier. A calculation function can then be checked with known inputs without simulating a keyboard.

Local variables normally exist within their block's scope. Do not return the address of an automatic local variable; its lifetime ends when the function returns. Use meaningful names such as count, capacity and total instead of assigning every variable a single letter.

## Reasoning in more depth
A function contract describes valid inputs, promised output and any side effects. Parameter values in C are passed by value. Changing a scalar parameter changes the local copy, while dereferencing a valid pointer can change an object owned elsewhere. Do not return a pointer to a local automatic object whose lifetime ends at return. Separating calculation from input/output makes functions easier to test.

## Independent task | Attempt before reading the answer
For int square(int x){return x*x;}, state the arithmetic precondition. Does calling square(a) change a?

## Worked answer and marking points
The product must be representable in int; otherwise signed overflow gives undefined behavior. A contract should restrict x accordingly or use checked arithmetic. Calling square(a) does not modify a because x is a local value copy. Save the result explicitly if needed. A wider return type alone does not widen the multiplication unless the operands are converted before multiplying.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 06 | Arrays, strings and bounds

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


# Session 07 | Pointers, structures and data ownership

## What you should be able to do
Reason about pointer validity, structure fields and object lifetime.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A pointer holds an address of an object or function, or a null pointer value, according to its type. &x obtains the address of x; *p accesses the pointed-to object when p is valid for that access. A pointer does not automatically make the pointed-to object's lifetime longer.

Worked example: int x=4; int *p=&x; *p=9; changes x to 9 because p points to x. In a swap function, pass addresses of the caller's variables and exchange the pointed-to values. Passing copies of the integers and swapping only those copies would leave the originals unchanged.

A struct groups related fields, such as a student identifier and mark. Use . for a structure object and -> for a pointer to a structure. Decide who owns a resource and when it remains valid. Dynamic memory obtained with malloc must be checked for allocation failure and later released with free when no longer needed; using freed storage or freeing it twice is invalid. This pack's core exercises use bounded arrays to keep introductory practice focused.

Do not memorize pointer syntax without drawing a small memory picture. Label the variable, the pointer and the object it refers to.

## Reasoning in more depth
A pointer value is useful only with a clear validity and lifetime contract. A null pointer is deliberately not an object address. A pointer can become invalid when the referenced object's lifetime ends, even if its bits appear unchanged. The address-of operator obtains an address and dereference accesses the referenced object. Structures group fields, but they do not automatically manage the lifetime of any pointers stored inside them.

## Independent task | Attempt before reading the answer
Trace int x=4; int *p=&x; *p=9;. State x and *p afterward. What must be true before evaluating *p?

## Worked answer and marking points
Both x and *p are 9 because p refers to x. Before dereference, p must designate a live object of an appropriate type with permitted access; merely being non-null is insufficient. If p were null, uninitialized or dangling, dereferencing it would not be a valid operation.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


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


## Practice set
1. Write an input-output contract for a function finding the minimum of three integers.
2. Predict 9/4, 9%4 and 9/4.0.
3. Why does double mean = sum/count fail when both operands are int and the total is not divisible by the count?
4. Write a correct condition for an integer between 10 and 20 inclusive.
5. Trace a loop adding 2,4,6 to an initially zero total. Show each state.
6. What is wrong with indexing a five-element array using i <= 5 starting at i=0?
7. How many elements are required to store "Mbeya" as a C string?
8. A function receives int *p and performs *p=12. Under what conditions can this change a caller's variable safely?
9. Why is returning the address of a local automatic int invalid for later access?
10. Design six tests for a mark parser accepting integers 0-100.
11. Explain how to avoid accidentally truncating a personal file in a file-writing exercise.
12. Build the supplied C examples, run their tests and modify one program to handle a new requirement. Record your change and a test for it.

## Answers and reasoning
1. Example: accepts three representable int values and returns a value no larger than any of them and equal to at least one input. Ties are valid.
2. 2,1,2.25. The first two use integer arithmetic; the third uses a floating-point operand.
3. Integer division happens before assignment. Use (double)sum/count after ensuring count is nonzero and the sum has not overflowed.
4. x >= 10 && x <= 20. Do not use a chained mathematical comparison.
5. Before iteration 1 total=0; after adding 2 total=2; after 4 total=6; after 6 total=12.
6. It attempts indices 0,1,2,3,4,5. Index 5 is outside the array. Use i < 5 for that range.
7. Six: five letters plus '\0'.
8. p must point to a live, writable int object that the caller allows the function to change. It must not be null, dangling or otherwise invalid.
9. The object's lifetime ends on return. An address value does not preserve that object's validity.
10. 0 and 100 accept; -1 and 101 reject; "abc" rejects; "42x" rejects. Also consider empty input and unusually long input when extending the parser.
11. Use a fresh sandbox directory and a fixed practice filename. Understand the file mode, check errors and never reuse an important existing path.
12. Evidence must include compiler output, expected/actual results and your changed source. A pass from the provided test runner verifies its listed cases, not every possible input or platform.

## Further study
Harvard CS50 C materials: https://cs50.harvard.edu/x/weeks/1/ . C language reference for precise semantics: WG14 N1570 committee draft, https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf . N1570 is a C11-era draft, not the latest language edition; these examples intentionally use the widely supported C17 mode and standard-library foundations. The practice files and explanations are original.
