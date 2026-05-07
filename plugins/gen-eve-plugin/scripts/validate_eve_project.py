"""Validate common IDM2040 EVE demo project issues.

The checks are intentionally desktop-safe: syntax parsing, tag duplication,
asset path references, and presence of return paths for demo loops.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


TAG_ASSIGN_RE = re.compile(r"^(tag_[A-Za-z0-9_]+)\s*=")
OPEN_ASSET_RE = re.compile(r"open\(\s*[\"']([^\"']+\.(?:jpg|jpeg|png|raw|avi))[\"']")


def project_root_from(start: Path) -> Path:
    """Return the repository root inferred from a script location."""
    for parent in [start, *start.parents]:
        if (parent / "IDM2040_demo").is_dir():
            return parent
    raise FileNotFoundError("Could not find IDM2040_demo from script path.")


def iter_python_files(root: Path) -> list[Path]:
    """Return all Python files under the IDM2040 demo tree."""
    return sorted((root / "IDM2040_demo").rglob("*.py"))


def check_syntax(root: Path) -> list[str]:
    """Return syntax errors for Python files."""
    errors = []
    for path in iter_python_files(root):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            rel = path.relative_to(root)
            errors.append(f"{rel}:{exc.lineno}: syntax error: {exc.msg}")
    return errors


def check_duplicate_tags(root: Path) -> list[str]:
    """Return duplicate tag name findings within individual files."""
    findings = []
    for path in iter_python_files(root):
        tags: dict[str, int] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            match = TAG_ASSIGN_RE.match(line)
            if match:
                tag = match.group(1)
                tags[tag] = tags.get(tag, 0) + 1
        for tag, count in sorted(tags.items()):
            if count > 1:
                findings.append(f"{path.relative_to(root)}: duplicate tag name {tag}")
    return findings


def asset_candidates(root: Path, source: Path, asset: str) -> list[Path]:
    """Return likely filesystem locations for a target asset reference."""
    demo_root = root / "IDM2040_demo"
    return [
        source.parent / asset,
        demo_root / asset,
        root / asset,
    ]


def check_assets(root: Path) -> list[str]:
    """Return missing literal asset path findings."""
    findings = []
    for path in iter_python_files(root):
        text = path.read_text(encoding="utf-8")
        for asset in OPEN_ASSET_RE.findall(text):
            if not any(candidate.exists() for candidate in asset_candidates(root, path, asset)):
                rel = path.relative_to(root)
                findings.append(f"{rel}: missing asset reference: {asset}")
    return findings


def check_exit_paths(root: Path) -> list[str]:
    """Return warnings for demo loop files without an obvious back or break path."""
    findings = []
    skip_names = {"code", "helper", "widgets", "tags", "__init__", "__Init__", "datetime"}
    for path in iter_python_files(root):
        if path.stem in skip_names:
            continue
        text = path.read_text(encoding="utf-8")
        if "while True" not in text and "while 1" not in text:
            continue
        has_exit_text = "Back" in text or "break" in text or "return -1" in text
        if not has_exit_text:
            findings.append(f"{path.relative_to(root)}: loop has no obvious Back/break path")
    return findings


def validate(root: Path) -> int:
    """Run validations and return a process status code."""
    findings = []
    findings.extend(check_syntax(root))
    findings.extend(check_duplicate_tags(root))
    findings.extend(check_assets(root))
    findings.extend(check_exit_paths(root))

    if findings:
        print("Validation findings:")
        for finding in findings:
            print(f"  - {finding}")
        return 1

    print("Validation passed.")
    return 0


def main() -> int:
    """Run the command-line validator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest parent with IDM2040_demo.",
    )
    args = parser.parse_args()

    root = args.root.resolve() if args.root else project_root_from(Path(__file__).resolve())
    return validate(root)


if __name__ == "__main__":
    raise SystemExit(main())
