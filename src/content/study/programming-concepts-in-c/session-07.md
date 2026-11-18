---
title: "Pointers, structures and data ownership"
module: "programming-concepts-in-c"
code: "CS 8138"
number: 7
objective: "Reason about pointer validity, structure fields and object lifetime."
---

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
