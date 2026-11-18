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
