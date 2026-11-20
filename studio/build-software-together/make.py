"""Six-slide invitation to learn software engineering through daily practice."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "export") + "/"
os.makedirs(OUT, exist_ok=True)

ART_STYLE = "print"
TOTAL = 6
POST_URL = "depriver.tech/blog/build-software-together/"
for shared in ("base.py", "kit.py", "editorial.py"):
    with open(os.path.join(STUDIO, shared)) as source:
        exec(compile(source.read(), source.name, "exec"))

s = page(1, "Open invitation")
title2(s, "Let’s build", "software together.", y=270, size=103)
s.para(M, 540, "Daily coding challenges, full-stack projects and practical software engineering skills.", f(MED, 38), W - 2 * M, 57, NAVY)
chat(s, M, 715, 800, "I’m curious about tech. Can I join if I’m just starting?", "You", mine=False, size=30, lh=42)
chat(s, 295, 875, 710, "Yes. Beginners are welcome.", "Build with us", size=30, lh=42)
horizon(s, 1)
cover_footer(s, "Swipe to see how it works")
finish(s)
s.save(1)

pages = [
    ("Learn together", "Bring what", "you’re learning.", [
        ("From class", "Bring a concept or exercise you want to practise."),
        ("From a course", "Share what you tried and where you got stuck."),
        ("From your own project", "Ask for a second pair of eyes on a bug or an idea."),
    ], "Study together", "Take turns explaining what you learned."),
    ("Daily practice", "One challenge.", "Every day.", [
        ("Get a short task", "We’ll post one daily, including weekends."),
        ("Try it when you’re free", "Share a solution, your progress or a question."),
        ("Meet when we can", "We’ll schedule online and in-person sessions together."),
    ], "Example challenge", "Add a filter that shows only unfinished assignments."),
    ("First full-stack project", "Build a", "study planner.", [
        ("Frontend", "Make a form to add assignments and due dates."),
        ("Backend", "Create an API to add and list assignments."),
        ("Database", "Save assignments and their completion status."),
    ], "Work as a team", "Rotate roles so everyone gets to try each part."),
    ("Career skills", "Build skills", "you can show.", [
        ("Work with Git", "Make small commits and open a pull request."),
        ("Review and test", "Give feedback and check that the feature works."),
        ("Explain your work", "Show a feature you built and why you built it that way."),
    ], "Portfolio goal", "Aim for a demo and a contribution you can talk through."),
]

for n, (label, first, second, rows, note, takeaway) in enumerate(pages, 2):
    s = page(n, label)
    title2(s, first, second, y=242, size=91)
    for index, (heading, copy) in enumerate(rows):
        y = 472 + index * 166
        card(s, (M, y, W - M - 9, y + 132))
        s.text(M + 30, y + 53, heading, f(BOLD, 34), NAVY)
        s.text(M + 30, y + 97, copy, f(REG, 26), GREY)
    horizon(s, n)
    navy_note(s, note, takeaway)
    finish(s)
    s.save(n)

s = page(TOTAL, "Join us")
title2(s, "Want to", "build with us?", y=270, size=104)
s.para(M, 550, "If you’re curious about tech or already building projects, you’re welcome.", f(MED, 38), W - 2 * M, 56, NAVY)
chat(s, M, 730, W - 2 * M - 8, "I’m in! I’d like to learn how to build an API.", "Send a message like this", size=32, lh=45)
s.text(M, 955, "Open the post and tap Join on WhatsApp.", f(SEMI, 33), NAVY)
horizon(s, TOTAL)
navy_note(s, "Join on WhatsApp via the post", POST_URL)
finish(s)
s.save(TOTAL)
