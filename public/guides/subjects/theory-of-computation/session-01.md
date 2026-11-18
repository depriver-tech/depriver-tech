# Session 01 | Sets, alphabets, strings and languages

## What you should be able to do
Distinguish strings, sets of strings and language operations.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An alphabet Sigma is a finite set of symbols, such as {0,1}. A string is a finite sequence of symbols from that alphabet. Its length is written |w|. The empty string, epsilon, has length zero. Sigma* is the set of all finite strings, including epsilon. A language over Sigma is any subset of Sigma*; it need not contain all strings or contain epsilon.

Worked example: Over Sigma={0,1}, let L be the strings that end in 01. Then 01, 101 and 1101 are in L, while epsilon, 0, 10 and 011 are not. State whether the empty string is accepted whenever its treatment affects your construction.

Concatenation joins strings in order. For u=10 and v=01, uv=1001, but vu=0110. Language union combines members; intersection keeps shared members. The empty language has no strings. It is different from {epsilon}, which has one member.

## Reasoning in more depth
A string is an ordered sequence; a language is a set, so duplicate members do not add new elements. The notation Sigma^n means all strings of exactly length n, whereas Sigma* includes every finite length. Concatenating languages forms every ordered combination of one string from each language. The empty string acts as the identity for string concatenation, but the empty language contributes no combinations.

## Independent task | Attempt before reading the answer
For A={0,01} and B={1,epsilon}, calculate AB and BA as sets.

## Worked answer and marking points
AB={01,0,011}; 01 arises in two ways but is listed once. BA={10,101,0,01}. Order changes the result. A{epsilon}=A, while concatenating A with the empty language gives the empty language.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
