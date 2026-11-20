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

# Ink illustrations share the grain and offset shadow used in the poster series.
SKETCHES = {
    "laptop": '<path fill="#fff9ef" d="M101 62 Q97 47 115 48 L470 57 Q489 58 488 76 L480 304 106 302Z"/><path fill="#a9c4f5" d="M124 74 L462 81 453 279 130 277Z"/><path fill="#fff9ef" d="M106 302 L480 304 546 354 Q548 372 513 379 L80 378 Q44 375 45 356Z"/><path d="M253 125l-62 54 63 53m90-108 58 54-57 56m-24-122-43 135m-49 103 123 1"/><path stroke="#e8603a" d="M496 111l44-27m-40 60 62-5m-67 38 46 25"/>',
    "notebook": '<path fill="#fff9ef" d="M298 118 Q216 51 78 87 L80 329 Q209 306 299 363 Q393 308 520 328 L519 87 Q388 57 298 118Z"/><path d="M298 118l1 245M118 137q90-13 144 29m-145 25q90-14 142 26m-140 24q86-12 142 30m75-104q71-33 144-28m-142 81q73-29 143-25m-141 78q69-27 142-24"/><path stroke="#e8603a" d="M134 288q63-8 111 21m89-177 37-12"/>',
    "calendar": '<path fill="#fff9ef" d="M104 84 L493 75 502 339 112 347Z"/><path fill="#a9c4f5" d="M104 84 L493 75 495 142 106 151Z"/><path d="M177 49l2 68m239-74 2 67m-270 90h300m-298 68h300m-232-95 3 145m67-147 4 146m68-147 2 144"/><path stroke="#e8603a" stroke-width="13" d="m308 226 15 14 31-34m-112 84 15 15 28-29m91 16 15 14 28-28"/>',
    "layers": '<path fill="#fff9ef" d="M87 72 L512 78 505 197 90 194Z"/><path d="M90 111l419 5m-385-24 8 1m22 0 8 1m22-1 8 1m74 49-28 17 28 16m72-34 28 17-28 18"/><path stroke="#e8603a" d="M301 198l-2 46m-16-18 16 19 16-18"/><path fill="#a9c4f5" d="M177 281 L177 342 Q301 398 426 340 L425 279Z"/><ellipse fill="#fff9ef" cx="301" cy="279" rx="124" ry="29"/><path d="M178 310q124 52 247-1"/>',
    "branch": '<path d="M125 313 Q115 217 127 109 M124 253 Q365 241 363 109 M368 232 Q487 220 487 145"/><circle fill="#fff9ef" cx="125" cy="313" r="35"/><circle fill="#a9c4f5" cx="124" cy="234" r="29"/><circle fill="#fff9ef" cx="127" cy="109" r="32"/><circle fill="#a9c4f5" cx="363" cy="109" r="34"/><circle fill="#fff9ef" cx="487" cy="145" r="29"/><path stroke="#e8603a" stroke-width="14" d="m330 306 51 41 100-96"/>',
    "message": '<path fill="#a9c4f5" d="M242 94 L488 89 Q528 91 532 124 L529 232 Q525 263 496 262 L468 263 488 311 427 262 245 266 Q212 264 210 234 L208 129 Q207 98 242 94Z"/><path fill="#fff9ef" d="M100 155 L357 149 Q397 150 401 187 L398 284 Q397 313 360 315 L194 317 126 365 146 316 100 317 Q68 318 68 282 L64 189 Q64 158 100 155Z"/><path stroke="#e8603a" stroke-width="15" d="m176 237 47 39 83-77"/>',
}
for key, paths in SKETCHES.items():
    ART[key] = svg(f'<g fill="none" stroke="#0b1e3f" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">{paths}</g>')


s = page(1, "Open invitation")
title2(s, "Let’s build", "software together.", y=270, size=103)
s.para(M, 540, "Daily coding challenges, full-stack projects and practical software engineering skills.", f(MED, 38), W - 2 * M, 57, NAVY)
chat(s, M, 715, 505, "I’m curious about tech. Can I join if I’m just starting?", "You", mine=False, size=30, lh=42)
chat(s, M, 885, 505, "Yes. Beginners are welcome.", "Build with us", size=30, lh=42)
paste_print(s, print_art("laptop", k(430)), 575, 718)
horizon(s, 1)
cover_footer(s, "Swipe to see how it works")
finish(s)
s.save(1)

pages = [
    ("notebook", "Learn together", "Bring what", "you’re learning.", [
        ("From class", "Bring a concept or exercise you want to practise."),
        ("From a course", "Share what you tried and where you got stuck."),
        ("From your own project", "Ask for a second pair of eyes on a bug or an idea."),
    ], "Study together", "Take turns explaining what you learned."),
    ("calendar", "Daily practice", "One challenge.", "Every day.", [
        ("Get a short task", "We’ll post one daily, including weekends."),
        ("Make time to practise", "Try each daily task. Share progress or ask for help."),
        ("Show up when you commit", "Meet online or in person. Let us know if plans change."),
    ], "Example challenge", "Add a filter that shows only unfinished assignments."),
    ("layers", "First full-stack project", "Build a", "study planner.", [
        ("Frontend", "Make a form to add assignments and due dates."),
        ("Backend", "Create an API to add and list assignments."),
        ("Database", "Save assignments and their completion status."),
    ], "Work as a team", "Rotate roles so everyone gets to try each part."),
    ("branch", "Career skills", "Build skills", "you can show.", [
        ("Work with Git", "Make small commits and open a pull request."),
        ("Review and test", "Give feedback and check that the feature works."),
        ("Explain your work", "Show a feature you built and why you built it that way."),
    ], "Portfolio goal", "Aim for a demo and a contribution you can talk through."),
]

for n, (art, label, first, second, rows, note, takeaway) in enumerate(pages, 2):
    s = page(n, label)
    title2(s, first, second, y=242, size=91)
    for index, (heading, copy) in enumerate(rows):
        y = 472 + index * 166
        card(s, (M, y, 650, y + 132))
        s.text(M + 30, y + 53, heading, f(BOLD, 34), NAVY)
        s.para(M + 30, y + 87, copy, f(REG, 24), 510, 30, GREY)
    paste_print(s, print_art(art, k(380)), 638, 552)
    horizon(s, n)
    navy_note(s, note, takeaway)
    finish(s)
    s.save(n)

s = page(TOTAL, "Join us")
title2(s, "Want to", "build with us?", y=270, size=104)
s.para(M, 550, "If you’re curious about tech or already building projects, you’re welcome.", f(MED, 38), W - 2 * M, 56, NAVY)
chat(s, M, 730, 560, "I’m in! I want to learn APIs. I’m usually free after 6.", "Send a message like this", size=32, lh=45)
paste_print(s, print_art("message", k(390)), 628, 680)
s.text(M, 970, "Share what you can commit to.", f(SEMI, 33), NAVY)
horizon(s, TOTAL)
navy_note(s, "Join on WhatsApp via the post", POST_URL)
finish(s)
s.save(TOTAL)
