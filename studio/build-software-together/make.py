"""Six-slide invitation to learn software engineering through daily practice."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "export") + "/"
os.makedirs(OUT, exist_ok=True)

ART_STYLE = "print"
POST_URL = "depriver.tech/blog/build-software-together/"
for shared in ("base.py", "kit.py", "editorial.py"):
    with open(os.path.join(STUDIO, shared)) as source:
        exec(compile(source.read(), source.name, "exec"))

TOTAL = 6

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


def illustration(s, key, width, x, y, tilt=0):
    art = print_art(key, k(width))
    if tilt:
        art = art.rotate(tilt, resample=Image.BICUBIC, expand=True)
    paste_print(s, art, x, y, offset=(12, 15), opacity=0.22)


def save(s, number):
    finish(s)
    s.save(number)


s = page(1, "An invitation from Privatus Cosmas")
s.text(M - 6, 271, "Let’s build", f(BOLD, 126), NAVY)
s.text(M - 7, 405, "software", f(BOLD, 142), NAVY)
s.text(M - 6, 535, "together.", f(BOLD, 126), ORANGE)
swash(s, M + 5, 641, 566, thick=10)
s.para(M, 668, "Daily coding challenges. Full-stack projects. People to learn with.", f(MED, 37), 395, 54, NAVY)
horizon(s, 1)
illustration(s, "laptop", 614, 421, 665, -8)
sticker(s, 274, 969, "Beginners welcome", angle=5, bg=BLUE, fg=NAVY, size=26)
cover_footer(s, "Swipe to see the plan")
save(s, 1)

s = page(2, "Learn together")
title2(s, "Bring what", "you’re learning.", y=250, size=94)
illustration(s, "notebook", 570, 235, 374, 5)
s.text(M, 826, "A lecture. A course. A side project.", f(BOLD, 42), NAVY)
s.para(M, 901, "Bring a question and show us what you’ve tried. We’ll work through it together.", f(MED, 33), 850, 48, GREY)
horizon(s, 2)
navy_note(s, "How we learn", "Take turns explaining what you learned.")
save(s, 2)

s = page(3, "Daily practice")
title2(s, "One challenge.", "Every day.", y=242, size=91)
illustration(s, "calendar", 446, 558, 419, -6)
s.para(M, 512, "We’ll post a short task every day, including weekends.", f(MED, 36), 477, 52, NAVY)
swash(s, M, 343, 665, thick=8)
s.text(M, 771, "Try it. Share progress. Ask for help.", f(BOLD, 43), NAVY)
s.para(M, 852, "We’ll plan online and in-person sessions together. Show up when you commit and tell us early if plans change.", f(MED, 32), 892, 47, GREY)
horizon(s, 3)
navy_note(s, "Example challenge", "Add a filter that shows only unfinished assignments.")
save(s, 3)

s = page(4, "First full-stack project")
title2(s, "Build a", "study planner.", y=242, size=94)
illustration(s, "layers", 515, 507, 493, 5)
numbered(s, [
    ("Frontend", "Make the assignment form."),
    ("Backend", "Create an API to add and list tasks."),
    ("Database", "Store assignments and due dates."),
], 522, maxw=490, gap=146, ts=40, bs=26)
s.para(M, 979, "Add a task, set its due date, then mark it done.", f(MED, 30), 900, 44, NAVY)
horizon(s, 4)
navy_note(s, "Work as a team", "Rotate roles so everyone gets to try each part.")
save(s, 4)

s = page(5, "Career skills")
title2(s, "Build skills", "you can show.", y=242, size=91)
illustration(s, "branch", 545, 243, 365, -3)
for x, heading, copy in [
    (M, "Commit", "Use Git to show how your work changed."),
    (395, "Review", "Read a teammate’s code and test it."),
    (714, "Demo", "Explain a feature you helped build."),
]:
    hairline(s, x, x + 271, 802, ORANGE, 4)
    s.text(x, 868, heading, f(BOLD, 39), NAVY)
    s.para(x, 921, copy, f(MED, 27), 275, 38, GREY)
horizon(s, 5)
navy_note(s, "Portfolio goal", "Aim for a demo and a contribution you can talk through.")
save(s, 5)

s = page(6, "Join us")
title2(s, "Want to", "build with us?", y=260, size=104)
s.para(M, 512, "Curious about tech? Tell me what you want to learn and what time you can commit.", f(MED, 37), 852, 56, NAVY)
illustration(s, "message", 440, 563, 635, -9)
chat(s, M, 685, 514, "I’m in! I want to learn APIs. I’m usually free after 6.", "Your first message", size=32, lh=45)
horizon(s, 6)
smallcaps(s, M, BASE + 80, "Open the post and tap", 18, SOFT)
s.text(M, BASE + 150, "Join on WhatsApp", f(BOLD, 50), WHITE_T)
s.text(M, BASE + 211, POST_URL, f(MED, 27), SOFT)
save(s, 6)
