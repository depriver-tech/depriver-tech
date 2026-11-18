# Individual subject guides

Original independent foundation material for seven semester-one subjects. The session sequence is proposed self-study, not a lecturer-issued timetable or complete syllabus. Module names/codes were checked against the supplied MUST Prospectus 2025/2026; current assessed coverage still requires lecturer outlines.

Sources: `notes/` contains the original module chapters; `session_enrichment.py` adds 56 original objectives, teaching extensions and independent tasks with reasoned answers. Further-study references are retained in the module PDFs. No private school records are included.

Build with Python containing ReportLab and pypdf:

```
python3 studio/subject-guides/build.py
```

This generates seven PDF books, editable subject/session Markdown, a ZIP, the study content collection and subject metadata. Website routes render the content collection using the existing Astro layout and saved theme system.

Validation performed 18 November 2026:

- All seven final 12-page PDFs rendered and visually reviewed; session boundaries and tables inspected.
- All 56 online session routes built with objectives, explanations, tasks and answers.
- New arithmetic, language-set, FIFO, page-translation, logic and circuit examples checked independently; the C examples compiled and executed with strict C17 warnings.
- Archive integrity and presence of seven PDFs verified.
- Browser flow: library to module to session; active session and previous/next links checked. Mobile reader at 390px had no horizontal document overflow.
