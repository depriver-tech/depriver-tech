# CS 8102 | Basics in Digital Circuit

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
Digital circuits use physical signals to represent discrete logical values. Learn to convert representations, reason with Boolean algebra, build combinational functions and explain how sequential circuits store state. This foundation module has eight sessions, original examples and a practice set. Use paper or a simulator unless your instructor supervises appropriate hardware work.

Prerequisites: powers of two, basic algebra and careful table reading. A logical 1 is an abstraction, not a universal voltage value. Valid voltage ranges depend on the logic family and supply.

## Session map
1. Number systems and representation
2. Binary arithmetic and two's complement
3. Gates and truth tables
4. Boolean algebra and equivalent circuits
5. From truth tables to simplified logic
6. Combinational building blocks
7. State, latches, flip-flops and counters
8. State machines, timing and verification

# Session 01 | Number systems and representation

## What you should be able to do
Convert representations while stating width and signedness.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
In base b, a digit's place value is a power of b. Binary uses 0 and 1; hexadecimal uses 0-9 and A-F. Hexadecimal is convenient because one hex digit corresponds exactly to four bits. Leading zeroes do not change an unsigned value, but the chosen width matters for arithmetic and signed interpretation.

Worked example: 45 decimal = 32+8+4+1, so its six-bit binary form is 101101. Group into four-bit blocks with leading zeroes: 0010 1101, giving hex 2D. Checking back, 2*16+13=45.

To convert a fractional binary value, use negative powers of two. 0.101 binary = 1/2 + 0/4 + 1/8 = 0.625 decimal. Not every decimal fraction has a finite binary representation. The stored bit pattern and its interpretation must be specified; the same bits can represent an unsigned integer, a signed integer or part of another encoding.

## Reasoning in more depth
A bit pattern alone does not specify its meaning. The same pattern can encode an unsigned number, a signed number, a character or an instruction under different conventions. Positional binary uses powers of two. Hexadecimal groups four bits per digit, making long patterns easier to read without changing their value. Leading zeroes preserve an unsigned value but can matter when the width is part of a signed representation.

## Independent task | Attempt before reading the answer
Convert unsigned binary 101101 to decimal and hexadecimal. Then interpret 11111111 as unsigned and as 8-bit two's complement.

## Worked answer and marking points
101101=32+8+4+1=45 decimal and 2D hexadecimal (0010 1101). 11111111 is 255 unsigned. As an 8-bit two's-complement value it is -1. State the interpretation before assigning meaning to the pattern.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 02 | Binary arithmetic and two's complement

## What you should be able to do
Perform fixed-width addition and distinguish carry from signed overflow.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Binary addition follows carry rules: 1+1 gives sum bit 0 and carry 1. For an n-bit unsigned value, the representable range is 0 through 2^n-1. An n-bit two's-complement value represents -2^(n-1) through 2^(n-1)-1. Interpret the most significant bit with negative weight when reading two's complement.

Worked example: In 8-bit two's complement, -5 is found by inverting 00000101 to 11111010 and adding 1, giving 11111011. Adding this to 00001001 (9) gives 1 00000100. Discarding the carry beyond 8 bits yields 00000100, which is 4.

Carry-out and signed overflow are different concepts. Adding 01111111 and 00000001 gives 10000000 in 8 bits: an unsigned result of 128 fits, but the signed mathematical result 128 is outside the two's-complement range, so signed overflow occurred. Always state width and interpretation before judging overflow.

## Reasoning in more depth
Unsigned overflow concerns a carry beyond the chosen width. Signed two's-complement overflow concerns a mathematical answer outside the signed range. Adding two positive operands and obtaining a negative sign indicates signed overflow; a final carry is not the signed-overflow criterion. Hardware can expose flags, while a programming language may assign different semantics to overflow, so do not transfer a circuit model into C without checking the language rules.

## Independent task | Attempt before reading the answer
Add 0111 and 0001 using four bits. Interpret the result as unsigned and signed two's complement.

## Worked answer and marking points
The four-bit result is 1000. Unsigned, 7+1=8 and no carry beyond four bits occurs. Signed four-bit values range -8 to 7, so +8 is unrepresentable; the pattern reads -8 and signed overflow occurred. The same bit addition has different conclusions under the two interpretations.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 03 | Gates and truth tables

## What you should be able to do
Derive a truth table from a gate expression rather than its visual shape.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
The basic logical operations include NOT, AND, OR and XOR. AND outputs 1 only when both inputs are 1. OR outputs 1 when at least one input is 1. XOR outputs 1 when exactly one of two inputs is 1. NAND negates AND; NOR negates OR; XNOR negates XOR.

| A | B | AND | OR | XOR | NAND |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 |

Worked example: An alarm activates when a door is open AND the system is armed. Let D=door-open and A=armed. The specification is Y=D AND A. A truth table prevents confusing this with OR, which would activate the alarm whenever the system was armed, even with a closed door.

Write the meaning of 0 and 1 for each input before building the table. A label such as "door" alone is ambiguous: does 1 mean open or closed?

## Reasoning in more depth
For n independent binary inputs, a complete truth table has 2^n rows. Evaluate inner expressions first and label intermediate columns when the logic is nested. A gate symbol or expression represents a function, not the physical timing of its implementation. Two ideal circuits with equal truth tables implement the same combinational function even when their propagation delays differ.

## Independent task | Attempt before reading the answer
Build the truth table for Y=NOT(A AND B). Which input rows make Y zero?

## Worked answer and marking points
For inputs 00,01,10,11 the AND outputs are 0,0,0,1 and Y outputs are 1,1,1,0. Only A=1 and B=1 makes Y zero. This is NAND. The negation applies to the entire AND result, not independently to just one input.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 04 | Boolean algebra and equivalent circuits

## What you should be able to do
Verify an algebraic simplification and apply De Morgan's law correctly.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Boolean algebra manipulates logic functions. Common laws include X+0=X, X*1=X, X+X=X, X*X=X, X+X'=1 and X*X'=0. Here + means OR, * means AND and ' means NOT; these symbols are not ordinary arithmetic in this context.

De Morgan's laws are (AB)'=A'+B' and (A+B)'=A'B'. They help convert between gate structures and reason about negated conditions. NAND and NOR are each functionally complete: suitable combinations can implement any Boolean function.

Worked example: Y=AB+AB'. Factor A to obtain A(B+B')=A*1=A. Four truth-table rows confirm that the output depends only on A. The simplified implementation needs only a connection carrying A, rather than redundant gates.

Be careful with distribution and negation. (A+B)' is not A'+B'. Write every complement over its intended expression, using parentheses in plain-text notes so the scope is unambiguous.

## Reasoning in more depth
Boolean algebra uses identities on binary values, so ordinary numeric intuition can mislead: A+A=A in OR notation. Apply De Morgan by complementing each term and exchanging AND with OR. Preserve parentheses until the scope of every complement is clear. You can verify a proposed simplification with a complete truth table for a small input count; one matching row is insufficient.

## Independent task | Attempt before reading the answer
Simplify Y=A OR (A AND B), and rewrite NOT(A OR B) using AND and complements.

## Worked answer and marking points
Absorption gives Y=A, since when A=1 the OR is already true and when A=0 both terms are false. De Morgan gives NOT A AND NOT B. The latter is true only for A=B=0. It is not the same as NOT A OR NOT B, which is false only when both inputs are 1.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 05 | From truth tables to simplified logic

## What you should be able to do
Construct a sum of products from the rows that require output one.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A sum-of-products expression ORs together terms that AND literals. To build one from a truth table, create a minterm for every row whose output is 1. For a row A=0,B=1,C=0, the minterm is A'BC'. Then simplify with algebra or a Karnaugh map when appropriate.

A Karnaugh map places adjacent cells in Gray-code order, so neighboring cells differ by one input bit. Group adjacent 1s into rectangular power-of-two groups, allowing wraparound where the map structure permits it. Larger groups remove more changing variables. A don't-care entry can be used only when the specification genuinely allows either output for that input.

Worked example: For inputs A,B,C, suppose Y=1 for minterms 1,3,5,7 under the binary index order ABC. These are 001,011,101,111. C is 1 in every row, while A and B vary over all combinations. The simplified function is Y=C.

A simplified expression is meaningful only if it still matches every required row. Verify it rather than trusting the visual shape of a group.

## Reasoning in more depth
A minterm is true for exactly one input row. Include each variable uncomplemented when its row value is 1 and complemented when it is 0, then OR the required minterms. Simplification should preserve the full specified truth table. Treat don't-care inputs as unspecified design freedom only when the specification really permits it; silently ignoring inconvenient rows changes the required behavior.

## Independent task | Attempt before reading the answer
For inputs A,B, Y is 1 on rows 01 and 11 only. Write the canonical sum of products and simplify.

## Worked answer and marking points
Y=(NOT A AND B) OR (A AND B). Factor B to obtain B AND (NOT A OR A)=B. The output depends only on B; checking rows 00,01,10,11 gives 0,1,0,1. No row was assumed to be a don't-care.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 06 | Combinational building blocks

## What you should be able to do
Relate multiplexers and adders to selection and arithmetic functions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A combinational circuit's outputs depend on its current inputs, allowing for propagation delay. A multiplexer selects an input according to control bits. A decoder maps an encoded input to selected outputs. Adders combine bits and carries. These blocks compose into larger datapaths.

Worked example: A two-input multiplexer with select S has Y=S'A+SB. If S=0, the expression reduces to A. If S=1, it reduces to B. This derivation is a clearer specification than memorizing a symbol without knowing which input each select value chooses.

A half adder has sum A XOR B and carry AB. A full adder also includes an incoming carry. One expression for its carry is AB + C_in(A XOR B); the sum is A XOR B XOR C_in. Test the all-ones row: 1+1+1=3, so sum=1 and carry=1.

In a ripple-carry adder, carries pass between stages. Correct Boolean outputs do not imply instantaneous operation; the worst-case carry path affects timing.

## Reasoning in more depth
A multiplexer selects among data inputs; its select bits determine which value reaches the output. A half adder combines two one-bit operands with a sum and carry. A full adder includes carry-in, allowing stages to be chained. Distinguish arithmetic weight: a carry contributes to the next higher bit position, so sum and carry cannot be read as two equal-weight outputs.

## Independent task | Attempt before reading the answer
For a full adder with A=1, B=1 and carry-in=1, find sum and carry-out. For a 2:1 mux with D0=0,D1=1, what happens as S changes?

## Worked answer and marking points
The arithmetic total is 3, binary 11: sum=1 and carry-out=1. For the mux, S=0 selects D0=0 and S=1 selects D1=1, so this wiring outputs S. The full-adder result represents sum+2*carry-out=3.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 07 | State, latches, flip-flops and counters

## What you should be able to do
Trace state changes at a clock edge and distinguish state from input.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A sequential circuit stores state, so its outputs or future behavior can depend on past inputs. A latch is level-sensitive under its control conditions; an edge-triggered flip-flop captures according to a clock edge and its timing requirements. A register groups storage elements, while a counter updates its stored value according to a rule.

Worked example: A two-bit binary counter cycles 00 -> 01 -> 10 -> 11 -> 00. For a synchronous next-state description, the low bit toggles each step; the high bit toggles when the old low bit is 1. Use the old state consistently when deriving next-state equations.

Reset behavior must be specified. Does reset act synchronously with the clock or asynchronously? Which state does it establish? Without these choices, two circuit descriptions may behave differently even if their normal counting sequence agrees.

Do not describe a flip-flop as "always copying the input." Its sampling behavior and clock conditions are the point of the abstraction.

## Reasoning in more depth
A flip-flop samples according to its timing contract, rather than continuously following every input change. For an ideal positive-edge D flip-flop, the next Q is D at the rising edge. Between sampling events the stored state remains unchanged, assuming no active asynchronous control. Real devices also require setup and hold timing; violating those conditions is not represented by a simple ideal truth table.

## Independent task | Attempt before reading the answer
An ideal D flip-flop starts with Q=0. D is 1 at the first rising edge, then becomes 0 before the second rising edge. Give Q just after each edge and between the edges.

## Worked answer and marking points
After the first rising edge Q=1. Changing D to 0 between edges leaves Q=1. After the second rising edge Q=0. This assumes D is stable for the required setup/hold intervals and that no reset or other control is active.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 08 | State machines, timing and verification

## What you should be able to do
Specify state transitions and check a timing budget with units.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A finite-state controller connects current state and inputs to next state, and possibly to outputs. In a Moore-style description, outputs depend on state; in a Mealy-style description, outputs can depend on state and current input. Specify which model you are using.

Worked example: A traffic-light teaching model has states Red, Green and Amber, with timer events moving Red -> Green -> Amber -> Red. Outputs are encoded by state. Real road-control systems need far more safety and timing logic; this simplified model is for understanding state transitions, not for deployment.

Propagation delay measures the time before an input change affects an output. Setup and hold requirements constrain when data must be stable around a sampling edge. A circuit can be logically correct but fail when timing constraints are violated. Hazards and glitches can occur when paths have different delays.

Verification routine: declare signal meanings, enumerate required input combinations or state transitions, predict outputs, simulate, compare and explain discrepancies. Keep a waveform or truth table as evidence. Changing a wire until the simulator appears quiet is not a substitute for a specification.

## Reasoning in more depth
A synchronous state machine combines a stored current state with combinational next-state logic. Define the reset state and what each input causes in each state, including unexpected cases. Timing analysis includes clock-to-Q delay, combinational delay and destination setup time, with appropriate clock uncertainty. A functionally correct transition table does not prove the circuit can run at an arbitrary clock rate.

## Independent task | Attempt before reading the answer
A path has clock-to-Q 2 ns, combinational delay 6 ns and setup time 1 ns. Ignoring skew and margin, find the minimum period and corresponding maximum frequency.

## Worked answer and marking points
The period must be at least 2+6+1=9 ns. The corresponding upper frequency bound is 1/(9e-9) Hz, about 111.1 MHz. This simplified bound omits skew, uncertainty and other paths; it is not a guaranteed operating frequency for a physical board.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


## Practice set
1. Convert decimal 26 to binary and hex.
2. Interpret 110010 as an unsigned binary value.
3. Represent -12 in 8-bit two's complement.
4. Add 0111 and 0001 as 4-bit numbers. Discuss unsigned and signed interpretation.
5. Complete the XOR truth table from memory.
6. Simplify A + AB and explain the law used.
7. Apply De Morgan's law to (A+B+C)'.
8. Build the sum-of-products expression for a two-input function that is 1 only for inputs 01 and 10.
9. Evaluate a 2:1 mux for A=0,B=1, first with S=0 and then S=1.
10. For A=1,B=0,C_in=1, find full-adder sum and carry.
11. List six successive states of a 2-bit counter starting from 10.
12. Explain why a truth table alone does not prove a clocked circuit meets timing requirements.

## Answers and reasoning
1. 26=16+8+2, so binary 11010; pad to 0001 1010 for hex 1A.
2. 32+16+2=50.
3. +12 is 00001100; invert to 11110011, add 1: 11110100.
4. The bit result is 1000. Unsigned 7+1=8 fits. Signed 4-bit values range -8 to 7, so adding +7 and +1 overflows and the stored pattern reads as -8.
5. For inputs 00,01,10,11 the outputs are 0,1,1,0.
6. A+AB=A by absorption. If A=1 the output is already 1; if A=0 both terms are 0.
7. A'B'C'. All OR terms become complemented AND terms.
8. A'B+AB', which is XOR. Include the complement on the input that is 0 in each selected row.
9. S=0 selects A, giving 0. S=1 selects B, giving 1.
10. 1+0+1=2, whose two-bit form is 10: sum=0, carry=1.
11. 10,11,00,01,10,11. State whether the starting value counts as the first listed state, as done here.
12. A truth table describes stable logical relationships. It does not quantify propagation delay or show whether data meets setup and hold requirements around clock edges.

## Further study and evidence
MIT Computation Structures has topic videos and worksheets: https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/ . Use it as a supporting course, not as proof that every topic appears in your current module. Produce one verified truth table, one simplified Boolean function and one counter waveform. The examples in this pack are original.
