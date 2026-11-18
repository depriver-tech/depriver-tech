# CS 8103 | Electrical Fundamentals

Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.

## Module route and preparation
This module builds the language needed to reason about voltage, current, resistance, power, simple circuits and elementary time-dependent behavior. Work through eight sessions and practise drawing a circuit before selecting equations. These are foundation notes based on the module title; your laboratory instructions and current syllabus take priority for assessed work.

Practical boundary: do the exercises on paper or in a circuit simulator. Physical experiments require appropriate instructor-approved low-voltage equipment and supervision. Do not use mains electricity, open power supplies or charge/discharge unknown capacitors as a self-study experiment. Measurement instructions here explain concepts, not authorization to work on live equipment.

## Session map
1. Quantities, units and physical meaning
2. Ohm's law and power
3. Series circuits and voltage division
4. Parallel circuits and current division
5. Kirchhoff's laws and nodal analysis
6. Capacitors and RC transients
7. Inductors and AC foundations
8. Measurement, uncertainty and checking answers

# Session 01 | Quantities, units and physical meaning

## What you should be able to do
Convert prefixes and distinguish charge flow from energy transfer.

## Preparation and session plan
Read the module preparation notes and identify any prerequisite you need to revise. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Charge Q is measured in coulombs (C). Current I is the rate of charge flow, measured in amperes (A). Voltage V is energy per unit charge, measured in volts (V). Resistance R relates voltage and current for an ohmic resistor under the applicable conditions, measured in ohms. Power P is the rate of energy transfer, measured in watts (W).

Prefixes matter: milli means 10^-3, micro means 10^-6, kilo means 10^3 and mega means 10^6. Convert consistently before substituting values. A factor-of-one-thousand error can make a neat-looking answer physically wrong.

Worked example: If 0.024 C passes a point in 0.006 s at a steady average rate, I=Q/t=4 A. If current is 4 mA instead, that is 0.004 A. The unit is part of the value, not optional decoration.

Conventional current direction follows the direction positive charge would move. Electron drift in a metal is opposite to that conventional direction. You can solve a circuit using either consistent convention, but do not change direction definitions midway through a calculation.

## Reasoning in more depth
Units make the physical claim explicit. Current is charge per time, voltage is energy per charge and power is energy per time. Convert prefixes before substituting unless the cancellation is deliberately tracked. A milliampere is 0.001 A; a kilohm is 1000 ohms. Check that a final unit follows from the formula rather than adding a familiar unit after an unexamined calculation.

## Independent task | Attempt before reading the answer
A current of 4 mA flows for 30 s. Find the transferred charge. If 3 J are transferred per coulomb, state the voltage.

## Worked answer and marking points
I=0.004 A and Q=It=0.004*30=0.12 C. Voltage is energy per charge, so 3 J/C=3 V. The current describes a rate of charge flow; the voltage describes energy per unit charge.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 02 | Ohm's law and power

## What you should be able to do
Use Ohm's law and power with consistent units and assumptions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
For an ohmic resistor in its valid operating conditions, V=IR. Rearranging gives I=V/R and R=V/I. This is not a universal relationship for every component: diodes, for example, do not behave like a constant resistance across all operating points.

Power transferred with the passive sign convention is P=VI, positive when the element absorbs power under the chosen voltage/current reference directions. For a resistor, combine Ohm's law to obtain P=I^2R=V^2/R. Energy over a constant-power interval is E=Pt.

Worked example: A 1.0 kOhm resistor has 5.0 V across it. I=5/1000=0.005 A=5 mA. Its dissipated power is 5*0.005=0.025 W=25 mW. The same result follows from 25/1000. Checking with a second expression can reveal a unit error.

A practical component has a power rating and may have temperature and voltage limits. A calculated current alone is not a complete component-selection procedure. In a paper exercise, state when you assume ideal components and constant temperature.

## Reasoning in more depth
For an ideal ohmic resistor, voltage and current are proportional at the modeled conditions. Real resistance may change with temperature and components have ratings and tolerances. Power can be calculated as VI, I^2R or V^2/R when the resistor relation applies. Agreement between two formulas is a useful arithmetic check but does not verify that an assumed ideal model matches a real component.

## Independent task | Attempt before reading the answer
For an ideal 1.5 kOhm resistor across 6 V, calculate current and power in two ways.

## Worked answer and marking points
R=1500 ohms. I=6/1500=0.004 A=4 mA. P=VI=6*0.004=0.024 W=24 mW. Also P=V^2/R=36/1500=0.024 W. These are paper-model values, not instructions to connect an unknown supply or component.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 03 | Series circuits and voltage division

## What you should be able to do
Calculate series current and predict the effect of loading a divider.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Resistors are in series when the same branch current must pass through each without an intervening branch carrying away current. Equivalent resistance is the sum. The voltage across each resistor is its current times its resistance, so the larger resistance receives the larger voltage drop for the same current.

Worked example: A 12 V ideal source drives 2 kOhm and 4 kOhm in series. Equivalent resistance is 6 kOhm, giving I=12/6000=2 mA. Voltage drops are 4 V and 8 V. Their sum is the source voltage.

The unloaded divider relation is V_out=V_in*R_bottom/(R_top+R_bottom), when output is measured across the bottom resistor and no extra load changes the circuit. Adding a load in parallel with the bottom resistor changes the effective bottom resistance. Do not use the unloaded formula unchanged after attaching a significant load.

A circuit's appearance on a drawing can be misleading. Identify nodes and connections rather than deciding "series" because two components are drawn next to each other.

## Reasoning in more depth
In a series path, the same current passes through each element. The total resistance is the sum, and each voltage drop follows its share of the total. The simple unloaded divider formula assumes no additional current leaves the midpoint. A connected load creates a parallel branch with the lower resistor, changing the equivalent resistance and usually reducing that midpoint voltage.

## Independent task | Attempt before reading the answer
A 12 V ideal source feeds two series 3 kOhm resistors. Find the midpoint voltage unloaded. Then connect an ideal 3 kOhm load across the lower resistor in the paper model.

## Worked answer and marking points
Unloaded, equal resistors divide 12 V equally, giving 6 V. With the load, the lower equivalent is 3k||3k=1.5 kOhm. Total is 4.5 kOhm, so midpoint=12*(1.5/4.5)=4 V. The load invalidates the original unloaded ratio.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 04 | Parallel circuits and current division

## What you should be able to do
Use a common branch voltage to calculate parallel resistance and currents.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Components are in parallel when they share both connection nodes and therefore have the same voltage across them. For resistors, 1/R_eq = 1/R1 + 1/R2 + ... . Two resistors give R_eq=R1R2/(R1+R2). For positive finite resistances, the equivalent is smaller than the smallest branch resistance.

Worked example: Put 3 kOhm and 6 kOhm across 12 V. Their currents are 4 mA and 2 mA. Total current is 6 mA, so equivalent resistance is 12/0.006=2 kOhm. The parallel formula gives the same result.

In a two-branch resistive current divider, a smaller resistance receives a larger current. If you forget the formula, calculate the common voltage or reason from I=V/R rather than guessing which resistance belongs in the numerator.

For a mixed series-parallel circuit, simplify an identifiable group, redraw the reduced circuit, and repeat. If the topology is not reducible by those patterns, use a more general method such as nodal analysis.

## Reasoning in more depth
Parallel components share the same two nodes, so their voltages match. Currents divide according to conductance: the smaller resistance carries more current under the same voltage. The equivalent resistance of positive parallel resistors is smaller than the smallest branch resistance. That inequality is a quick error check when a reciprocal sum has been inverted incorrectly.

## Independent task | Attempt before reading the answer
Two ideal resistors, 2 kOhm and 6 kOhm, are in parallel across 6 V. Calculate branch currents, total current and equivalent resistance.

## Worked answer and marking points
Branch currents are 6/2000=3 mA and 6/6000=1 mA. Total is 4 mA. Equivalent resistance is 6/0.004=1500 ohms=1.5 kOhm. This is below 2 kOhm, as expected. The current ratio is inverse to the resistance ratio.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 05 | Kirchhoff's laws and nodal analysis

## What you should be able to do
Choose a reference node and solve a one-unknown nodal equation.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Kirchhoff's current law (KCL) balances charge at a node: with consistent signs, currents entering and leaving sum to zero in the lumped-circuit model. Kirchhoff's voltage law (KVL) balances voltage changes around a closed loop under the conditions of that circuit model. Reference directions can be chosen; a negative answer often means the actual direction opposes the chosen reference.

Worked example: A node V connects through 2 kOhm to an ideal 10 V node and through 3 kOhm to ground. Taking currents leaving the unknown node gives (V-10)/2000 + V/3000 = 0. Multiply by 6000: 3(V-10)+2V=0, so 5V=30 and V=6 V. Current from the 10 V node is (10-6)/2000=2 mA, equal to 6/3000 leaving to ground.

A nodal-analysis routine: choose a reference node, label unknown node voltages, write each resistor current as a voltage difference divided by resistance, apply KCL, solve, then check currents and power. The reference node defines zero potential for the calculation; it does not imply zero current everywhere connected to it.

## Reasoning in more depth
A node voltage is relative to a chosen reference, not an absolute property of a point in isolation. Set current directions consistently, express branch currents with Ohm's law and apply Kirchhoff's current law. A negative current result indicates that the actual direction opposes your chosen arrow; it does not automatically mean an algebra error. Substitute the answer into the node equation to check balance.

## Independent task | Attempt before reading the answer
A node V connects to a 10 V node through 2 kOhm and to reference 0 V through 3 kOhm. Write KCL and solve for V.

## Worked answer and marking points
Using outward currents, (V-10)/2000+V/3000=0. Multiplying by 6000 gives 3V-30+2V=0, so V=6 V. Current from the 10 V node is (10-6)/2000=2 mA; current to reference is 6/3000=2 mA. Incoming and outgoing currents agree.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 06 | Capacitors and RC transients

## What you should be able to do
Use an RC time constant and recognize initial and final conditions.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
A capacitor stores energy in an electric field. For the ideal capacitor relation Q=CV, capacitance C is measured in farads. Current is i=C*dv/dt under a consistent reference convention. An ideal capacitor's voltage cannot jump instantaneously without an impulse of current in the idealized model.

For a simple RC step response, the time constant is tau=RC. Charging from 0 toward a constant source V_s through R gives v_C(t)=V_s*(1-exp(-t/tau)). Discharging from V_0 through R gives v_C(t)=V_0*exp(-t/tau), for the appropriate simple circuit and initial conditions.

Worked example: R=10 kOhm and C=100 microfarads give tau=10000*0.0001=1 s. Charging toward 5 V from zero gives about 3.16 V at 1 s, because 1-exp(-1) is about 0.632. It approaches 5 V asymptotically; it does not jump to 5 V at exactly one time constant.

Stored energy is E=0.5*C*V^2. A disconnected capacitor can retain energy. That is why unknown stored-energy components are outside unsupervised self-study practice.

## Reasoning in more depth
A capacitor's voltage cannot jump in an ideal model without an impulse of current. For a step through a resistor, the time constant tau=RC controls how quickly the voltage approaches its final value. At one time constant, charging has reached about 63.2% of the total change. The exponential approaches the final value asymptotically, so five time constants is a practical approximation rather than exact completion.

## Independent task | Attempt before reading the answer
An initially uncharged 100 uF ideal capacitor charges through 10 kOhm toward 5 V. Find tau and the capacitor voltage at t=tau.

## Worked answer and marking points
Convert C=100e-6 F and R=10000 ohms. tau=RC=1 s. v(tau)=5*(1-exp(-1)) is about 3.16 V. Initially v=0; as time grows it approaches 5 V. The unit ohm*farad equals seconds.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 07 | Inductors and AC foundations

## What you should be able to do
Relate an ideal sinusoid's frequency, period, RMS value and reactive behavior.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An ideal inductor stores energy in a magnetic field. Its voltage is v=L*di/dt, with inductance L in henries. Its current cannot change instantaneously without an impulse of voltage in the ideal model. Energy is E=0.5*L*I^2. These relations are different from the resistor's constant proportional relationship.

A sinusoidal voltage can be written v(t)=V_peak*sin(2*pi*f*t+phi), where frequency f is in hertz and period T=1/f. For a sine wave with no DC offset, V_rms=V_peak/sqrt(2). RMS is useful for comparing resistive heating; it is not the same as the arithmetic mean of the waveform over a whole cycle.

Worked example: A 50 Hz sine wave has period 1/50=0.02 s=20 ms. If its peak is 10 V, RMS is about 7.07 V. Across a pure 100 Ohm resistor, average power is V_rms^2/R=0.5 W.

In AC analysis, reactance introduces frequency dependence and phase. For simple sinusoidal steady-state models, X_L=2*pi*f*L and X_C=1/(2*pi*f*C). Do not apply a purely resistive formula blindly to mixed AC loads. Phasor methods are a next topic if required by your lecturer.

## Reasoning in more depth
Frequency counts cycles per second; angular frequency is 2*pi*f radians per second. RMS is defined through a mean square and square root; the peak divided by sqrt(2) rule applies to a sinusoid, not every waveform. Inductors resist changes in current, while capacitors resist changes in voltage in their ideal models. Their AC impedance depends on frequency, so a DC resistance-only model is insufficient.

## Independent task | Attempt before reading the answer
For an ideal 50 Hz sinusoidal voltage with peak 10 V, calculate period, angular frequency and RMS voltage.

## Worked answer and marking points
Period T=1/50=0.020 s=20 ms. Angular frequency=2*pi*50=100*pi rad/s, about 314.16 rad/s. RMS=10/sqrt(2), about 7.07 V. These are analysis quantities only; do not treat the frequency as authorization to work on mains circuits.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


# Session 08 | Measurement, uncertainty and checking answers

## What you should be able to do
Compare measurements with a model and express an approximate tolerance range.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
An ideal voltmeter measures across two points and has infinite input resistance. An ideal ammeter measures branch current in series and has zero resistance. Real instruments differ from these ideals and can alter the circuit. Connecting a current-measurement input across a voltage source is not a valid substitute for measuring voltage and may create a dangerous short circuit.

For safe self-study, use a simulator to practise instrument placement. For physical measurements, follow the supervised lab's range, connection and equipment procedures. A continuity or resistance measurement is ordinarily performed on appropriately isolated, unpowered circuitry under those procedures, not on a live unknown circuit.

Worked example: A nominal 1000 Ohm resistor measures 980 Ohm. The difference from nominal is -20 Ohm; its magnitude relative to nominal is 2%. Compare this with specified tolerance and instrument uncertainty before judging it. Do not call every difference an experimental mistake.

Check every calculation in three ways: dimensions, magnitude and conservation. A parallel resistance greater than both positive branches is suspicious. In a simple resistor loop, voltage drops should balance the source. Source power supplied should match total power absorbed under your sign convention, within the model and rounding.

## Reasoning in more depth
A measured value includes instrument limits, resolution and setup effects as well as the component's actual behavior. Keep more digits during intermediate calculations than you report at the end. A tolerance interval is not automatically a probability distribution. Compare a result with a plausible range before blaming the instrument or component. Practical measurements belong in supervised appropriate low-voltage labs or simulation, following local instructions.

## Independent task | Attempt before reading the answer
An ideal nominal 1 kOhm resistor has a stated tolerance of plus/minus 5%. Give its allowed resistance interval and the current interval under an exactly 5 V paper-model source.

## Worked answer and marking points
Resistance lies from 950 to 1050 ohms. Current is largest at the smallest resistance: 5/950 about 5.26 mA. It is smallest at 1050 ohms: 5/1050 about 4.76 mA. The inverse relation means simply attaching plus/minus 5% to the nominal current is only an approximation.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.


## Practice set
1. Convert 4.7 kOhm, 220 microfarads and 15 mA to base units.
2. Find current through 2 kOhm with 6 V across it.
3. Find power dissipated in that resistor using two formulas.
4. An ideal 9 V source drives 1 kOhm and 2 kOhm in series. Find current and both voltage drops.
5. Find the equivalent of 1 kOhm and 1 kOhm in parallel.
6. Across 10 V, parallel branches are 2 kOhm and 5 kOhm. Find both currents and total current.
7. An unloaded divider has R_top=3 kOhm, R_bottom=1 kOhm and V_in=8 V. Find V_out.
8. Write KCL for a node connected to 12 V through 2 kOhm and to ground through 4 kOhm. Solve for the node voltage.
9. Find tau for R=5 kOhm and C=200 microfarads.
10. A capacitor charges from zero toward 10 V. Approximately what voltage is reached at one time constant?
11. Find the period and RMS voltage of a 100 Hz sine wave with peak 8 V.
12. Explain correct conceptual placement of a voltmeter and ammeter, and why "it has numbers on the display" does not prove the measurement is valid.

## Answers and reasoning
1. 4700 Ohm; 0.000220 F; 0.015 A.
2. I=6/2000=0.003 A=3 mA.
3. VI=6*0.003=0.018 W. V^2/R=36/2000=0.018 W, or 18 mW.
4. Total R=3000 Ohm; I=3 mA. Drops: 3 V across 1 kOhm and 6 V across 2 kOhm; their sum is 9 V.
5. Equal branches give half either resistance: 500 Ohm.
6. I1=10/2000=5 mA; I2=10/5000=2 mA; total 7 mA.
7. 8*1000/(3000+1000)=2 V. This assumes no loading at the output.
8. (V-12)/2000+V/4000=0. Multiply by 4000: 2V-24+V=0, so V=8 V. Both branch-current magnitudes are 2 mA.
9. 5000*0.0002=1 s.
10. About 6.32 V, using 10*(1-exp(-1)).
11. T=0.01 s=10 ms. V_rms=8/sqrt(2), approximately 5.66 V.
12. A voltmeter connects across the voltage of interest; an ammeter belongs in series with the branch. Correct mode, range, connections and instrument characteristics matter. A displayed value can reflect a wrong or unsafe setup.

## Further study and evidence
MIT Circuits and Electronics: https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/ . OpenStax University Physics Volume 2, current chapter: https://openstax.org/books/university-physics-volume-2/pages/9-1-electrical-current . The examples above were created for this pack. Submit a labeled circuit sketch, a complete calculation with units and a short explanation of your checks for each problem you solve.
