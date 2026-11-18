# CS 8103 | Electrical Fundamentals

## Learning outcomes and route
This module builds the language needed to reason about voltage, current, resistance, power, simple circuits and elementary time-dependent behavior. Work through eight lessons and practise drawing a circuit before selecting equations. These are foundation notes based on the module title; your laboratory instructions and current syllabus take priority for assessed work.

Practical boundary: do the exercises on paper or in a circuit simulator. Physical experiments require appropriate instructor-approved low-voltage equipment and supervision. Do not use mains electricity, open power supplies or charge/discharge unknown capacitors as a self-study experiment. Measurement instructions here explain concepts, not authorization to work on live equipment.

## Lesson 1 | Quantities, units and physical meaning
Charge Q is measured in coulombs (C). Current I is the rate of charge flow, measured in amperes (A). Voltage V is energy per unit charge, measured in volts (V). Resistance R relates voltage and current for an ohmic resistor under the applicable conditions, measured in ohms. Power P is the rate of energy transfer, measured in watts (W).

Prefixes matter: milli means 10^-3, micro means 10^-6, kilo means 10^3 and mega means 10^6. Convert consistently before substituting values. A factor-of-one-thousand error can make a neat-looking answer physically wrong.

Worked example: If 0.024 C passes a point in 0.006 s at a steady average rate, I=Q/t=4 A. If current is 4 mA instead, that is 0.004 A. The unit is part of the value, not optional decoration.

Conventional current direction follows the direction positive charge would move. Electron drift in a metal is opposite to that conventional direction. You can solve a circuit using either consistent convention, but do not change direction definitions midway through a calculation.

## Lesson 2 | Ohm's law and power
For an ohmic resistor in its valid operating conditions, V=IR. Rearranging gives I=V/R and R=V/I. This is not a universal relationship for every component: diodes, for example, do not behave like a constant resistance across all operating points.

Power transferred with the passive sign convention is P=VI, positive when the element absorbs power under the chosen voltage/current reference directions. For a resistor, combine Ohm's law to obtain P=I^2R=V^2/R. Energy over a constant-power interval is E=Pt.

Worked example: A 1.0 kOhm resistor has 5.0 V across it. I=5/1000=0.005 A=5 mA. Its dissipated power is 5*0.005=0.025 W=25 mW. The same result follows from 25/1000. Checking with a second expression can reveal a unit error.

A practical component has a power rating and may have temperature and voltage limits. A calculated current alone is not a complete component-selection procedure. In a paper exercise, state when you assume ideal components and constant temperature.

## Lesson 3 | Series circuits and voltage division
Resistors are in series when the same branch current must pass through each without an intervening branch carrying away current. Equivalent resistance is the sum. The voltage across each resistor is its current times its resistance, so the larger resistance receives the larger voltage drop for the same current.

Worked example: A 12 V ideal source drives 2 kOhm and 4 kOhm in series. Equivalent resistance is 6 kOhm, giving I=12/6000=2 mA. Voltage drops are 4 V and 8 V. Their sum is the source voltage.

The unloaded divider relation is V_out=V_in*R_bottom/(R_top+R_bottom), when output is measured across the bottom resistor and no extra load changes the circuit. Adding a load in parallel with the bottom resistor changes the effective bottom resistance. Do not use the unloaded formula unchanged after attaching a significant load.

A circuit's appearance on a drawing can be misleading. Identify nodes and connections rather than deciding "series" because two components are drawn next to each other.

## Lesson 4 | Parallel circuits and current division
Components are in parallel when they share both connection nodes and therefore have the same voltage across them. For resistors, 1/R_eq = 1/R1 + 1/R2 + ... . Two resistors give R_eq=R1R2/(R1+R2). For positive finite resistances, the equivalent is smaller than the smallest branch resistance.

Worked example: Put 3 kOhm and 6 kOhm across 12 V. Their currents are 4 mA and 2 mA. Total current is 6 mA, so equivalent resistance is 12/0.006=2 kOhm. The parallel formula gives the same result.

In a two-branch resistive current divider, a smaller resistance receives a larger current. If you forget the formula, calculate the common voltage or reason from I=V/R rather than guessing which resistance belongs in the numerator.

For a mixed series-parallel circuit, simplify an identifiable group, redraw the reduced circuit, and repeat. If the topology is not reducible by those patterns, use a more general method such as nodal analysis.

## Lesson 5 | Kirchhoff's laws and nodal analysis
Kirchhoff's current law (KCL) balances charge at a node: with consistent signs, currents entering and leaving sum to zero in the lumped-circuit model. Kirchhoff's voltage law (KVL) balances voltage changes around a closed loop under the conditions of that circuit model. Reference directions can be chosen; a negative answer often means the actual direction opposes the chosen reference.

Worked example: A node V connects through 2 kOhm to an ideal 10 V node and through 3 kOhm to ground. Taking currents leaving the unknown node gives (V-10)/2000 + V/3000 = 0. Multiply by 6000: 3(V-10)+2V=0, so 5V=30 and V=6 V. Current from the 10 V node is (10-6)/2000=2 mA, equal to 6/3000 leaving to ground.

A nodal-analysis routine: choose a reference node, label unknown node voltages, write each resistor current as a voltage difference divided by resistance, apply KCL, solve, then check currents and power. The reference node defines zero potential for the calculation; it does not imply zero current everywhere connected to it.

## Lesson 6 | Capacitors and RC transients
A capacitor stores energy in an electric field. For the ideal capacitor relation Q=CV, capacitance C is measured in farads. Current is i=C*dv/dt under a consistent reference convention. An ideal capacitor's voltage cannot jump instantaneously without an impulse of current in the idealized model.

For a simple RC step response, the time constant is tau=RC. Charging from 0 toward a constant source V_s through R gives v_C(t)=V_s*(1-exp(-t/tau)). Discharging from V_0 through R gives v_C(t)=V_0*exp(-t/tau), for the appropriate simple circuit and initial conditions.

Worked example: R=10 kOhm and C=100 microfarads give tau=10000*0.0001=1 s. Charging toward 5 V from zero gives about 3.16 V at 1 s, because 1-exp(-1) is about 0.632. It approaches 5 V asymptotically; it does not jump to 5 V at exactly one time constant.

Stored energy is E=0.5*C*V^2. A disconnected capacitor can retain energy. That is why unknown stored-energy components are outside unsupervised self-study practice.

## Lesson 7 | Inductors and AC foundations
An ideal inductor stores energy in a magnetic field. Its voltage is v=L*di/dt, with inductance L in henries. Its current cannot change instantaneously without an impulse of voltage in the ideal model. Energy is E=0.5*L*I^2. These relations are different from the resistor's constant proportional relationship.

A sinusoidal voltage can be written v(t)=V_peak*sin(2*pi*f*t+phi), where frequency f is in hertz and period T=1/f. For a sine wave with no DC offset, V_rms=V_peak/sqrt(2). RMS is useful for comparing resistive heating; it is not the same as the arithmetic mean of the waveform over a whole cycle.

Worked example: A 50 Hz sine wave has period 1/50=0.02 s=20 ms. If its peak is 10 V, RMS is about 7.07 V. Across a pure 100 Ohm resistor, average power is V_rms^2/R=0.5 W.

In AC analysis, reactance introduces frequency dependence and phase. For simple sinusoidal steady-state models, X_L=2*pi*f*L and X_C=1/(2*pi*f*C). Do not apply a purely resistive formula blindly to mixed AC loads. Phasor methods are a next topic if required by your lecturer.

## Lesson 8 | Measurement, uncertainty and checking answers
An ideal voltmeter measures across two points and has infinite input resistance. An ideal ammeter measures branch current in series and has zero resistance. Real instruments differ from these ideals and can alter the circuit. Connecting a current-measurement input across a voltage source is not a valid substitute for measuring voltage and may create a dangerous short circuit.

For safe self-study, use a simulator to practise instrument placement. For physical measurements, follow the supervised lab's range, connection and equipment procedures. A continuity or resistance measurement is ordinarily performed on appropriately isolated, unpowered circuitry under those procedures, not on a live unknown circuit.

Worked example: A nominal 1000 Ohm resistor measures 980 Ohm. The difference from nominal is -20 Ohm; its magnitude relative to nominal is 2%. Compare this with specified tolerance and instrument uncertainty before judging it. Do not call every difference an experimental mistake.

Check every calculation in three ways: dimensions, magnitude and conservation. A parallel resistance greater than both positive branches is suspicious. In a simple resistor loop, voltage drops should balance the source. Source power supplied should match total power absorbed under your sign convention, within the model and rounding.

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
