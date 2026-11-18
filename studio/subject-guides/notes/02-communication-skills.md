# HS 8101 | Communication Skills

## Learning outcomes and route
Communication in computing means helping a specific audience understand something accurately and act on it. This module develops purposeful reading, clear paragraphs, technical explanations, reports, source use, email, presentations and collaborative feedback. Work through eight lessons and produce the written evidence requested. This is an original foundation course, not an official assessment guide.

Prerequisites: willingness to revise and to explain an idea in your own words. You can plan an explanation in English or Kiswahili, but follow the language and format required by your lecturer for submission.

## Lesson 1 | Purpose, audience and channel
Before writing, answer three questions: Who will read this? What do they already know? What should they understand or do afterwards? A lecturer assessing a lab needs a reproducible method and evidence. A classmate trying to install a compiler needs ordered instructions and a way to verify success. A manager approving a change needs the problem, options, consequences and recommendation.

A channel should fit the purpose. A short email works for a clear request; a diagram can explain relationships; a report records evidence; a live conversation helps resolve ambiguity. Do not assume more technical vocabulary makes writing more professional.

Worked example: "The application has issues" gives no decision-useful information. A clearer defect report is: "On the registration page, submitting an empty email field creates an account instead of showing a validation message. Expected: reject the form and explain the missing field. Reproduced in three attempts." It separates observation from expectation without inventing a cause.

Task: Explain a C loop to two audiences: a new student and an experienced programmer. Change the explanation, not the underlying truth.

## Lesson 2 | Active reading and useful notes
Read with a question. First preview headings, definitions and examples. Then read a short section closely. Close it and reconstruct the main idea from memory. Finally, compare your reconstruction with the source and correct gaps. Copying paragraphs is a record of reading, not evidence of understanding.

Use a note structure with four fields: concept, own explanation, original example, question remaining. Record the source immediately so you can return to it. Mark uncertainties explicitly; a question mark is better than a confident error that becomes part of your revision.

Worked example: After reading about processes, write: "A process is an executing program with its own execution context and resources. Two launches of the same executable can be two processes. Question: what is shared between threads in one process?" This is more useful than copying a definition without an example.

For revision, turn a heading into a retrieval question. Replace "Ohm's law" with "When is V=IR a suitable model, and how do I check the units?"

## Lesson 3 | Sentences and paragraphs
A useful sentence makes its actor, action and object clear. Prefer a concrete verb: "The program validates the input" is clearer than "Input validation is carried out by the program." Passive voice is still useful when the action or result matters more than the actor, as in a method description.

A paragraph develops one main point. It often begins with a topic sentence, follows with explanation or evidence, and ends by connecting the point to its purpose. Every sentence should contribute to that point. Split paragraphs when the subject changes.

Worked example: "We tested it and it was okay" becomes: "The program correctly classified 0, 50 and 100 as valid marks. It rejected -1 and 101. These boundary tests support the input-range check; they do not establish that every possible input is handled correctly." Notice the limited, precise claim.

Editing pass: remove repeated ideas, vague "this" references, unnecessary introductions and unexplained abbreviations. Keep qualifications that affect meaning. Shorter is useful only if the result remains accurate.

## Lesson 4 | Explaining a technical process
Explain the purpose before the mechanism. Introduce required terms, show the steps, then demonstrate with a small example. Distinguish what is always true from what holds only under stated assumptions. Use units, input ranges and expected outputs where relevant.

Worked example: To explain an average, first say it distributes the total equally across the count. Then show 10+20+30=60; divide by 3 to get 20. In C, explain that integer division discards the fractional part of a nonnegative result, so a real-valued average requires a floating-point operation. The concept and the language behavior are related but different ideas.

For instructions, start each step with an action and include a check: "Compile the file with the command shown. If compilation succeeds, run the executable. Confirm that the output is 20.00." Avoid "click there" without naming the control. A screenshot can support an instruction but should not be the only source of information.

## Lesson 5 | Reports and evidence
Follow the structure required by the assignment. A typical lab report includes title, objective, relevant background, apparatus or software, method, results, discussion, conclusion and references. Results state what was observed or calculated. Discussion interprets the result, considers errors and limitations, and compares it with the intended model. The conclusion answers the objective using the evidence actually collected.

Worked example: A resistor experiment might report nominal resistance 1.0 kOhm and measured resistance 0.98 kOhm. The absolute difference is 0.02 kOhm; relative to the nominal value it is 2%. This is not automatically a malfunction. The discussion needs resistor tolerance, instrument resolution and test conditions. Do not invent measurements to make a report look complete.

A reproducible method names enough detail for another person to repeat it. For a program, record source-file version, compiler flags, test inputs and outputs. For a circuit calculation, show the diagram, assumptions, equations, substitutions and units.

## Lesson 6 | Summarizing, paraphrasing and citing
A summary selects the main points and is shorter than its source. A paraphrase restates a specific idea using your own sentence structure and wording. Neither removes the obligation to credit the source when the idea came from someone else. A quotation preserves the exact words and must be marked and cited; use quotations sparingly.

A practical workflow is read, close, write, compare, cite. Closing the source makes it harder to merely exchange a few words. Compare for accuracy, then add the source using the required referencing style. Keep the author or organization, title, year where available, URL or publication information, and any page or section needed to locate the claim.

Worked example: If an operating-systems textbook explains virtual memory, a report can cite that textbook for the concept and separately label your own diagram and example. Do not claim that a generated explanation is a verified source. Check factual claims against reliable material and follow the institution's rules on assistance and academic integrity.

## Lesson 7 | Professional email and collaborative communication
Use a specific subject, a courteous greeting, a concise context, a clear request and a close. Supply the details the recipient needs, but avoid unnecessary personal information. Send a follow-up after a reasonable interval appropriate to the deadline; do not interpret silence as approval.

Worked example:

Subject: CS 8138: clarification on file-input format

Dear Lecturer,
I am working on the file-processing exercise. The brief names a marks file but does not state whether each line contains one mark or a student name followed by a mark. Could you confirm the required format? I have attached the relevant part of the brief for context.
Thank you,
Privatus Cosmas

For group work, record decisions, owners and due dates. "Someone will finish the report" is not an assignment. "Asha will draft the method by Friday; Juma will check the results table on Saturday" makes responsibility visible. Use actual agreed names and dates, not assumptions.

## Lesson 8 | Presentations, listening and feedback
A presentation needs a clear question, a small number of supporting points and a conclusion the audience can remember. Begin with the problem, show one concrete example, then explain the result. Slides should support speech rather than reproduce an essay. Label diagrams and keep enough contrast and text size for the room.

Practise to time. A three-minute explanation might allocate 30 seconds to context, 90 seconds to the example, 40 seconds to interpretation and 20 seconds to the takeaway. These are planning proportions, not compulsory rules. Rehearse with a timer and adjust to your actual pace.

Worked example: Present the integer-division bug by showing the expected average, the original expression, its actual output and the corrected expression. Ask the audience to predict the result before revealing it. During questions, restate the question to check understanding. Say what you know and what needs checking; guessing is not professionalism.

Useful feedback describes the artifact and its effect: "The graph lacks units, so I cannot interpret the slope." It is more actionable than "This is bad." Listen without interrupting, clarify the requested change and decide how to revise.

## Practice set | Produce evidence
1. State an audience and intended action for a compiler-installation guide.
2. Rewrite: "The system is very good and works perfectly."
3. Write a four-sentence paragraph explaining why boundary tests matter.
4. Turn "memory management" into three retrieval questions.
5. Separate observation and inference: "The app crashed because the database is broken."
6. Design a results table for five C test cases.
7. Explain the difference between results and discussion in a lab report.
8. Outline a citation record for an online textbook chapter.
9. Write a professional email asking a lecturer to clarify an ambiguous submission format.
10. Create a three-minute presentation outline on a topic from another module.
11. Give constructive feedback on a diagram with no labels or units.
12. Write a 150-word explanation of one concept, then shorten it by about one third without losing essential meaning.

## Answer guide and assessment rubric
1. Example: first-year students who need to compile and run one C file. Intended action: run a supplied command and verify the expected output. Specify the operating system.
2. Replace praise with evidence: "The program passed the five listed tests. Performance and invalid-file handling have not yet been evaluated." The exact claim depends on actual tests.
3. Include a topic sentence, a boundary example such as 0 and 100, an explanation of what these cases can expose, and a limit on the conclusion. Do not claim that five tests prove every case.
4. Examples: What does virtual memory give a process? How does an address translate? Why can a page fault be expensive? Questions should require an explanation, not only a term.
5. Observation: the app crashed. Inference: a database problem caused it. State the steps, error message and evidence needed before assigning cause.
6. Columns: case ID, input, expected result, actual result, pass/fail and explanation. A useful test table makes disagreement visible.
7. Results document findings. Discussion explains their meaning, limitations and relation to the objective. A screenshot alone rarely supplies an adequate discussion.
8. Record organization or author, title, date if present, chapter or section, URL and access date when required by the selected style. Use the lecturer's specified citation format.
9. A strong answer includes a specific subject, relevant context, one answerable question, courtesy and identification. Do not invent an emergency or blame the lecturer.
10. A strong outline has one central idea, one worked example, clearly timed sections and a final takeaway. Demonstrate the explanation aloud.
11. Example: "Please label both axes and add voltage/current units. Without them I cannot tell whether the plotted slope represents resistance or conductance."
12. Assess accuracy, audience fit, structure, evidence and concision, each from 0 to 2. A score is a self-assessment aid, not an institutional grade. Compare drafts and identify one concrete improvement.

## Further study and weekly artifact
Read Google Technical Writing One, https://developers.google.com/tech-writing/one , and Purdue OWL's paragraph guidance, https://owl.purdue.edu/owl/general_writing/academic_writing/paragraphs_and_paragraphing/index.html . Use the sources as further reading; all examples in this pack are original.

Keep one revised artifact each week: email, explanation, test report, diagram caption or presentation outline. Preserve the first draft so improvement is visible.
