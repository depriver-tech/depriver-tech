---
title: "Measurement, uncertainty and checking answers"
module: "electrical-fundamentals"
code: "CS 8103"
number: 8
objective: "Compare measurements with a model and express an approximate tolerance range."
---

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
