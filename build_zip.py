"""
Utility script to bundle the repository into a ZIP archive.

Usage:
    python build_zip.py

This will create `context-engineering-starter-kit.zip` in the current directory.
"""

from __future__ import annotations

import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZIP_NAME = "context-engineering-starter-kit.zip"


def should_include(path: Path) -> bool:
    # Exclude virtual environments, git metadata, and generated output.
    parts = set(path.parts)
    if ".git" in parts or ".venv" in parts or "venv" in parts:
        return False
    if "output" in parts:
        return False
    if path.name.endswith(".zip"):
        return False
    return True


def build_zip() -> None:
    zip_path = ROOT / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dir_path = Path(dirpath)
            for filename in filenames:
                file_path = dir_path / filename
                if not should_include(file_path):
                    continue
                rel_path = file_path.relative_to(ROOT)
                zf.write(file_path, rel_path.as_posix())
    print(f"Created {zip_path}")


if __name__ == "__main__":
    build_zip()
