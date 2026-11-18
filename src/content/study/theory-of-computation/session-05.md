---
title: "Regular expressions and closure"
module: "theory-of-computation"
code: "CS 8101"
number: 5
objective: "Interpret formal regular expressions as whole-string specifications."
---

## What you should be able to do
Interpret formal regular expressions as whole-string specifications.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
In formal-language notation, union is often written with |, concatenation by adjacency, and repetition by *. The star permits zero repetitions. These are mathematical regular expressions; features such as backreferences in some programming-language regex engines go beyond this model.

Worked example: (0|1)*01 describes all binary strings ending in 01. The starred prefix can be any binary string, including epsilon. By contrast, (01)* describes epsilon, 01, 0101 and so on. They are different languages.

Regular languages are closed under union, intersection, concatenation, star and complement relative to the chosen Sigma*. For complementing a DFA, first ensure that its transition function is total, adding a sink if necessary, then exchange accepting and nonaccepting states. Forgetting the alphabet or missing transitions can give a wrong complement.

For intersection, a product construction tracks both DFA states at once. Accept when both components accept. A state pair means "where both machines would be after reading the same prefix."

## Reasoning in more depth
A formal regular expression denotes an entire language, unlike a search operation that may find a match inside a larger string. Fix the alphabet before using complement. To combine two DFA requirements, a product state records both machines' states for the same prefix; acceptance can require both, either or another stated combination. This construction connects logical conditions to machine memory.

## Independent task | Attempt before reading the answer
Over {0,1}, describe the language of 0(0|1)*1 and give its shortest member, two other members and two nonmembers.

## Worked answer and marking points
It consists of strings starting in 0 and ending in 1, with length at least 2. The shortest is 01. Examples include 001 and 0101. Nonmembers include epsilon and 010. The star allows an empty middle but does not remove the explicit first and last symbols.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
