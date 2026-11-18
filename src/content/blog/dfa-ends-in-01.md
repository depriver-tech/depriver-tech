---
title: "Read a DFA like a program: binary strings ending in 01"
description: "Build a three-state machine by deciding what each state remembers, then trace accepted and rejected strings instead of memorizing circles and arrows."
date: 2026-11-18
status: live
tags: ["students", "programming", "study", "theory"]
---

A finite automaton becomes easier to understand when every state has a job. Start by asking what the machine needs to remember about the part of the input already read.

Our language is simple: all strings over `{0,1}` that end in `01`. Examples include `01`, `101` and `1001`. The empty string, `0`, `10` and `010` are not members.

## Give the states meanings

- `q0`: no useful suffix has been retained.
- `q1`: the prefix read so far ends in `0`.
- `q2`: the prefix read so far ends in `01`.

Start in `q0`. Make only `q2` accepting. A DFA decides acceptance **after all input has been consumed**, not merely because it visited an accepting state earlier.

## Build the transition table

| State | Read 0 | Read 1 |
|---|---|---|
| q0 | q1 | q0 |
| q1 | q1 | q2 |
| q2 | q1 | q0 |

Why does `q1` on another `0` stay in `q1`? Because the latest symbol still provides the useful suffix `0`. Why does `q2` on `1` return to `q0`? The input now ends in `11`, so it no longer ends in either useful suffix.

*Usichore mishale kwa kubahatisha.* Do not guess the arrows. Explain what must still be true after every transition.

## Trace one accepted and one rejected string

For `1001`:

`q0 -> q0 -> q1 -> q1 -> q2`

The final state is accepting, so the string is accepted.

For `010`:

`q0 -> q1 -> q2 -> q1`

The machine visited `q2`, but the final state is `q1`. Reject. This distinction is a common source of wrong answers.

The empty string is rejected because no symbols are read and the start state `q0` is not accepting.

## A small proof is better than a pile of guesses

For each state, check that its stated meaning holds initially and is preserved by reading either symbol. Once the entire string has been consumed, that meaning tells you why `q2` corresponds exactly to the required ending.

Testing short strings helps find mistakes, but the state-meaning argument is what explains all lengths. Try `00101`, `011`, `000` and `1101` yourself before checking the final states.

The same language has the formal regular expression `(0|1)*01`: an arbitrary binary prefix followed by `01`. This is not the same as `(01)*`, which repeats the whole two-symbol block and includes the empty string.

## Continue studying

The free [semester-one study book](/guides/computer-science-semester-one.pdf) includes a full theory chapter with DFA/NFA foundations, regular expressions, grammars, a pumping-lemma example and practice answers. The [editable companion pack](/guides/computer-science-semester-one.zip) adds a study plan and retrieval cards.

For a deeper independently published course, see [MIT Automata, Computability, and Complexity](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/). Match the depth to your lecturer's current syllabus.
