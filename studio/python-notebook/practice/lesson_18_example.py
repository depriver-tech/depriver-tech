# 23 / Automation & office work
from pathlib import Path

folder = Path("practice_output")
for path in sorted(folder.glob("*.txt")):
    if path.is_file():
        print(path.name, path.stat().st_size, "bytes")
