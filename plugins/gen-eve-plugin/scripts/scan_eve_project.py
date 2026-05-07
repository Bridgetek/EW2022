"""Scan IDM2040 EVE demo project structure.

This script is safe to run on desktop Python. It does not import the target
CircuitPython modules; it only reads source files and reports useful metadata.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


PIN_RE = re.compile(r"\bboard\.(GP\d+)\b")
FLASH_RE = re.compile(r"\bcmd_flashread\s*\(")
LOAD_RE = re.compile(r"\bcmd_loadimage\s*\(")
TAG_ASSIGN_RE = re.compile(r"^(tag_[A-Za-z0-9_]+)\s*=")


def project_root_from(start: Path) -> Path:
    """Return the repository root inferred from a script location."""
    for parent in [start, *start.parents]:
        if (parent / "IDM2040_demo").is_dir():
            return parent
    raise FileNotFoundError("Could not find IDM2040_demo from script path.")


def iter_python_files(root: Path) -> list[Path]:
    """Return all Python files under the IDM2040 demo tree."""
    return sorted((root / "IDM2040_demo").rglob("*.py"))


def parse_defs(path: Path) -> tuple[list[str], list[str]]:
    """Return top-level class and function names from a Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return [], []

    classes = []
    functions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return classes, functions


def scan(root: Path) -> int:
    """Print project metadata and return a process status code."""
    demo_root = root / "IDM2040_demo"
    if not demo_root.is_dir():
        print(f"Missing demo directory: {demo_root}")
        return 1

    py_files = iter_python_files(root)
    print(f"Project root: {root}")
    print(f"Python files: {len(py_files)}")
    print()

    print("Demos:")
    for child in sorted(demo_root.iterdir()):
        if child.is_dir() and any(child.glob("*.py")):
            print(f"  - {child.name}")
    print()

    print("Tags:")
    tag_file = demo_root / "main_menu" / "tags_all.py"
    if tag_file.exists():
        for line in tag_file.read_text(encoding="utf-8").splitlines():
            match = TAG_ASSIGN_RE.match(line)
            if match:
                print(f"  - {match.group(1)}")
    else:
        print("  tags_all.py not found")
    print()

    pins: dict[str, set[str]] = {}
    flash_users = []
    load_users = []
    for path in py_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)
        for pin in PIN_RE.findall(text):
            pins.setdefault(pin, set()).add(str(rel))
        if FLASH_RE.search(text):
            flash_users.append(str(rel))
        if LOAD_RE.search(text):
            load_users.append(str(rel))

    print("Board pins:")
    for pin, files in sorted(pins.items(), key=lambda item: int(item[0][2:])):
        print(f"  - {pin}: {', '.join(sorted(files))}")
    print()

    print("EVE flash users:")
    for path in flash_users:
        print(f"  - {path}")
    print()

    print("Local image load users:")
    for path in load_users:
        print(f"  - {path}")
    print()

    print("Top-level definitions:")
    for path in py_files:
        classes, functions = parse_defs(path)
        if classes or functions:
            rel = path.relative_to(root)
            names = [f"class {name}" for name in classes]
            names.extend(f"def {name}" for name in functions)
            print(f"  - {rel}: {', '.join(names)}")

    return 0


def main() -> int:
    """Run the command-line scanner."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest parent with IDM2040_demo.",
    )
    args = parser.parse_args()

    root = args.root.resolve() if args.root else project_root_from(Path(__file__).resolve())
    return scan(root)


if __name__ == "__main__":
    raise SystemExit(main())
