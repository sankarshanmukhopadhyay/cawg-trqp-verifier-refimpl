from pathlib import Path


def walk(root: Path, prefix: str = "") -> list[str]:
    entries = sorted([p for p in root.iterdir()], key=lambda p: (p.is_file(), p.name))
    lines = []
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(walk(entry, prefix + extension))
    return lines


if __name__ == "__main__":
    root = Path(".")
    print(".")
    for line in walk(root):
        print(line)
