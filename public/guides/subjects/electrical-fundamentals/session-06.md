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
