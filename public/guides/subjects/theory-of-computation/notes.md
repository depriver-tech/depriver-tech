# CS 8101 | Theory of Computation

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
This module asks what computational models can recognize, what problems are solvable in principle, and how we reason about those claims. Learn to specify a language, build and trace finite automata, translate simple regular expressions, read grammars and distinguish computability from efficiency. The eight sessions form a foundation route; the lecturer's outline determines assessment depth.

Prerequisites: sets, functions, logical statements and simple proofs. A machine diagram without a precise language description is not a complete specification.

## Session map
1. Sets, alphabets, strings and languages
2. Deterministic finite automata
3. State meaning is more useful than guessing circles
4. Nondeterminism and subset construction
5. Regular expressions and closure
6. Why some languages need more memory
7. Grammars and pushdown intuition
8. Computability and complexity are different questions

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


# Session 02 | Deterministic finite automata

## What you should be able to do
Use a state invariant to justify a complete DFA.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A DFA has a finite set of states Q, an alphabet Sigma, a transition function delta: Q x Sigma -> Q, a start state q0 and a set F of accepting states. Each state-symbol pair has exactly one next state. A string is accepted if, after consuming all its symbols, the machine is in an accepting state.

Worked example: Recognize binary strings with an even number of 1s. Use E for even and O for odd. Start in E, and make E accepting. Reading 0 leaves the parity unchanged; reading 1 toggles E and O.

| State | Input 0 | Input 1 | Accepting? |
| --- | --- | --- | --- |
| E (start) | E | O | Yes |
| O | O | E | No |

Trace 1011: E -> O -> O -> E -> O, so reject. Trace 1010: E -> O -> O -> E -> E, so accept. Epsilon is accepted because the initial number of 1s is zero, which is even.

## Reasoning in more depth
A state invariant describes what is true after every consumed prefix, including the empty prefix. For parity, the transition on 1 changes parity and the transition on 0 preserves it. Induction has a base case at the start state and a preservation step for each input symbol. This reasoning explains all lengths; a few successful traces only check selected examples.

## Independent task | Attempt before reading the answer
Design a DFA accepting binary strings with an odd number of 1s. Trace 10101 and explain the empty-string decision.

## Worked answer and marking points
Use E and O. Start E; accept only O. On 0 stay, on 1 toggle. For 10101 the trace is E,O,O,E,E,O, so accept. Epsilon ends at E and is rejected. The invariant is parity of the number of 1s consumed, preserved by both transition rules.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 03 | State meaning is more useful than guessing circles

## What you should be able to do
Derive states from the suffix information required by a specification.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
When designing a DFA, state what information must be remembered from the prefix already read. For "ends in 01," remember whether the current suffix is empty or irrelevant, is 0, or is 01. These are meanings of states, not just labels.

Worked example: q0 means no useful suffix; q1 means the prefix ends in 0; q2 means it ends in 01. Start in q0 and accept only q2.

| State | Input 0 | Input 1 |
| --- | --- | --- |
| q0 | q1 | q0 |
| q1 | q1 | q2 |
| q2 | q1 | q0 |

Trace 1001: q0 -> q0 -> q1 -> q1 -> q2, so accept. Trace 010: q0 -> q1 -> q2 -> q1, so reject. Repeated zeroes matter: from q1 on 0, stay in q1 because the most recent symbol still gives a useful 0 suffix.

To justify the construction, explain how each transition preserves the stated meaning. Then test short accepted and rejected strings, including epsilon. Tests help find mistakes; an invariant argument explains all input lengths.

## Reasoning in more depth
For suffix recognition, keep the longest suffix of the consumed input that is also a prefix of the target pattern. When the target is 01, the useful partial matches are empty, 0 and 01. A new symbol can destroy a complete match or start a new partial one. Acceptance depends on the state after all input, so reaching an accepting state early does not guarantee the final string is accepted.

## Independent task | Attempt before reading the answer
Use the ends-in-01 DFA to trace 0101 and 011. Explain why they differ despite both containing 01.

## Worked answer and marking points
0101 follows q0,q1,q2,q1,q2 and accepts. 011 follows q0,q1,q2,q0 and rejects. The final 1 in 011 destroys the required suffix. The specification is ends in 01, not contains 01.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 04 | Nondeterminism and subset construction

## What you should be able to do
Carry out a concrete subset construction including an empty subset.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An NFA may allow several next states for a symbol, or none. Some definitions also permit epsilon transitions that consume no input. A string is accepted when at least one complete path consumes the string and ends in an accepting state. It is not necessary for every path to accept.

Worked example: To recognize strings containing 01 somewhere, an NFA can remain in a scanning state while reading any symbol, branch to a second state after seeing a 0, then enter an accepting state when the next symbol is 1. Once the substring has been found, it may consume remaining symbols in an accepting loop.

Subset construction converts an NFA to a DFA. A DFA state represents a set of possible NFA states. Start with the epsilon closure of the NFA start state; for each symbol, collect reachable states and then take epsilon closure again. A subset is accepting if it contains at least one NFA accepting state. Include the empty subset when it is reachable; it acts as a rejecting sink.

Nondeterminism changes the description, but DFAs and NFAs recognize the same class of languages: the regular languages. This does not mean that every language is regular.

## Reasoning in more depth
Each subset state represents every location the NFA could occupy after the same consumed prefix. Compute a union of outgoing transitions; do not select a single convenient path. An NFA state with no transition contributes nothing. A reachable empty subset loops to itself on every symbol and is rejecting. Epsilon closure is needed only when the NFA definition includes epsilon transitions.

## Independent task | Attempt before reading the answer
Over {a}, let start s have delta(s,a)={s,t}, and t have no outgoing transitions. Only t accepts. Build the reachable DFA subsets and decide epsilon, a and aa.

## Worked answer and marking points
Start subset {s} rejects. On a it reaches {s,t}, which accepts. From {s,t}, a reaches {s,t} again because s branches and t contributes nothing. Thus epsilon rejects, a and aa accept; indeed every positive number of a symbols accepts. No empty subset is reachable in this particular construction.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 05 | Regular expressions and closure

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


# Session 06 | Why some languages need more memory

## What you should be able to do
Use the quantifier order of the pumping lemma correctly.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A finite automaton has a fixed amount of state memory, regardless of input length. Some tasks require keeping track of unbounded information. The language {0^n 1^n : n >= 0} requires matching the number of zeroes and ones, and is not regular.

The pumping lemma gives a necessary property of regular languages. If L is regular, there is a pumping length p such that every sufficiently long string s in L can be split s=xyz with |xy| <= p, |y| > 0 and xy^i z in L for all i >= 0. To prove nonregularity using it, assume regularity, choose a suitable string, and handle every permitted decomposition.

Worked example: Choose s=0^p1^p. Every valid y lies among the first p zeroes and contains at least one zero. Pumping down with i=0 removes zeroes but no ones, so the result is not in L. This contradicts the required property.

Do not use the lemma backwards: finding one pumpable string does not establish regularity. A regular-language construction, such as a DFA, is a more direct positive proof.

## Reasoning in more depth
The pumping length is supplied by the assumed regularity; you do not get to choose its numerical value. You choose a string after learning p, but an opponent may choose any decomposition satisfying the length restrictions. Your argument must defeat all of them using an allowed pumping exponent. A proof that only one convenient split fails leaves other splits available and therefore proves nothing about regularity.

## Independent task | Attempt before reading the answer
Explain why choosing y=0^p is unnecessary when proving {0^n1^n} nonregular. What is enough to know about y?

## Worked answer and marking points
For s=0^p1^p, every valid y is 0^k for some k>=1, since |xy|<=p. Pumping down removes k zeroes while retaining p ones. The counts differ for every possible k, so the proof works without selecting a specific decomposition.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 07 | Grammars and pushdown intuition

## What you should be able to do
Trace a context-free derivation and relate it to stack behavior.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A grammar generates strings using production rules. A context-free grammar has a single nonterminal on the left of each rule. Derivation repeatedly replaces a nonterminal using an available production. A parse tree records the structure of the derivation.

Worked example: S -> 0S1 | epsilon generates exactly 0^n1^n for n >= 0. To derive 0011: S -> 0S1 -> 00S11 -> 0011. Each use of 0S1 adds one zero at the front and one one at the back. The epsilon rule stops the expansion.

A pushdown automaton adds a stack, which provides a last-in, first-out form of unbounded memory. For 0^n1^n, push a marker for each 0 and pop one for each 1, enforcing the correct phase order. This explains why the language can be context-free even though it is not regular.

Ambiguity means that some string has more than one parse tree or appropriate derivation structure. A grammar for arithmetic may need precedence and associativity rules; recognizing valid tokens is not enough to determine the intended expression structure.

## Reasoning in more depth
The grammar S -> 0S1 | epsilon makes the matching dependency explicit: each recursive expansion adds a pair and the base case stops. A derivation is a sequence of rule applications; a parse tree shows nested structure. A pushdown strategy must reject a 0 after the 1 phase begins, even when total counts happen to match. Balanced counts alone do not enforce the required order.

## Independent task | Attempt before reading the answer
Derive 000111, then explain why 0101 is not generated even though it contains two zeroes and two ones.

## Worked answer and marking points
S -> 0S1 -> 00S11 -> 000S111 -> 000111. Every generated string places all zeroes before all ones because expansion nests around S. In 0101 a zero appears after a one; equal totals cannot overcome that ordering violation.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 08 | Computability and complexity are different questions

## What you should be able to do
Separate decision, recognition and practical resource bounds.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A Turing-machine model adds an unbounded tape and a head that can read, write and move. It is a mathematical model, not a claim that real computers have infinite physical memory. A decider halts on every input and answers yes or no. A recognizer must accept members, but may run forever on some nonmembers.

The halting problem asks whether an arbitrary program halts on an arbitrary input. There is no algorithm that correctly decides all such program-input pairs. This does not mean that we can never prove a particular program halts; simple bounded loops are often easy to analyze.

Complexity asks about resource use, such as time or memory, for a solvable task as input size grows. A linear scan has a different growth pattern from checking all subsets. Being computable does not automatically mean being practical. Big-O gives an asymptotic upper bound, not the exact running time on a particular laptop.

Worked comparison: Determining whether a finite binary string ends in 01 is decidable and can be handled by a DFA. Proving that a general-purpose halting checker cannot exist concerns impossibility across all programs. These are fundamentally different kinds of claims.

## Reasoning in more depth
An algorithm can be guaranteed to finish yet require too many steps for a large input. A recognizer for a language is weaker than a decider because it need not terminate on nonmembers. When discussing an impossible general algorithm, specify the universal claim; it does not forbid solving restricted cases. Complexity also requires an input-size model: scanning n characters and scanning every subset of n items are different growth rates.

## Independent task | Attempt before reading the answer
Classify: a DFA simulation on a finite string; exhaustive testing of all subsets of n items; and a proposed checker that decides halting for every program/input pair.

## Worked answer and marking points
A DFA simulation is decidable and can scan a length-n string in O(n) time in the usual model. Exhaustive subset search is finite and thus can terminate, but enumerates 2^n subsets before accounting for per-subset work. A universally correct halting decider is impossible. These illustrate efficiency, termination and impossibility as separate issues.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


## Practice set
1. Distinguish epsilon, the empty language, and {epsilon}.
2. List all binary strings of length exactly 2.
3. Trace 11010 through the even-ones DFA. Accept or reject?
4. Trace 00101 through the ends-in-01 DFA.
5. Design a DFA for strings with an odd number of 0s. State whether epsilon is accepted.
6. Give a formal regular expression for binary strings starting with 1 and ending with 0.
7. Is epsilon in (01)*? Is 010 in it? Explain.
8. How do you identify accepting states during subset construction?
9. What must you fix before complementing an incomplete DFA?
10. Give a derivation of 000111 using S -> 0S1 | epsilon.
11. Explain why the pumping argument for 0^n1^n must consider every allowed split.
12. Distinguish a decider, a recognizer, and an efficient algorithm.

## Answers and reasoning
1. Epsilon is a string of length zero. The empty language has no members. {epsilon} has one member, the empty string.
2. 00, 01, 10 and 11. There are 2^2=4 possibilities.
3. E -> O -> E -> E -> O -> O. Reject: three 1s were read.
4. q0 -> q1 -> q1 -> q2 -> q1 -> q2. Accept: the final suffix is 01.
5. Use Even0 and Odd0. Start in Even0; accept Odd0. On 0 toggle; on 1 stay. Reject epsilon because zero zeroes is even.
6. 1(0|1)*0. The shortest accepted string is 10. A one-symbol string cannot satisfy both required endpoints here.
7. Epsilon is included by zero repetitions. 010 is not a whole number of repetitions of 01.
8. A subset state accepts if it contains any accepting state of the NFA. Do not require every state in the subset to accept.
9. Make transitions total over the declared alphabet, using a rejecting sink for missing transitions, then swap final/nonfinal states.
10. S -> 0S1 -> 00S11 -> 000S111 -> 000111.
11. The lemma allows a decomposition to exist if the language is regular. To contradict it, the chosen string must fail for all valid decompositions; disproving one arbitrary split is insufficient.
12. A decider always halts with a decision. A recognizer may fail to halt on nonmembers. Efficiency concerns the resources an algorithm uses; termination alone does not establish a useful resource bound.

## Mastery checkpoint and further study
Build a new DFA from a precise specification, state the meaning of every state and trace five strings. Explain why your construction handles all prefixes. Then contrast finite-state memory with stack memory using your own example.

Further study: MIT Automata, Computability, and Complexity, https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/ . The original lessons here are a foundation pathway; consult the course notes and your lecturer for formal proof depth.
