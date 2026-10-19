# 14 / Files and paths
from pathlib import Path

folder = Path("practice_output")
folder.mkdir(exist_ok=True)
path = folder / "notes.txt"
path.write_text("Learn Python\nTry a project\n",
                encoding="utf-8")
with path.open(encoding="utf-8") as handle:
    for line in handle:
        print(line.strip())
