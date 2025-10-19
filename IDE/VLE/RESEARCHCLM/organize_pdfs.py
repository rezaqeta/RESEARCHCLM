from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
CASE_DIR = ROOT / "case_study"
OTHER_DIR = ROOT / "other_sources"


def build_case_map(json_path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not json_path.exists():
        return mapping
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Warning: failed to parse {json_path.name}: {exc}")
        return mapping
    for entry in data:
        if not isinstance(entry, dict):
            continue
        filename = entry.get("filename")
        excel_name = (entry.get("excel_file") or "").strip().lower()
        if not filename:
            continue
        key = filename.lower()
        if excel_name == "climate_behavioral_change_papers.xlsx":
            mapping[key] = "case_study"
        elif key not in mapping:
            mapping[key] = "other_sources"
    return mapping


def looks_like_case_study(name: str) -> bool:
    lower_name = name.lower()
    if lower_name.endswith(".pdf"):
        lower_name = lower_name[:-4]
    normalized = lower_name.replace("_", " ").replace("-", " ")
    if "case study" in normalized:
        return True
    if "case" in normalized and "study" in normalized:
        return True
    return False


def pick_destination(pdf: Path, case_map: Dict[str, str]) -> Path:
    filename_key = pdf.name.lower()
    if filename_key in case_map:
        return CASE_DIR if case_map[filename_key] == "case_study" else OTHER_DIR
    if looks_like_case_study(pdf.name):
        return CASE_DIR
    return OTHER_DIR


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> None:
    ensure_directory(CASE_DIR)
    ensure_directory(OTHER_DIR)
    case_map = build_case_map(ROOT / "download_tasks.json")
    moved: List[Tuple[Path, Path]] = []
    skipped: List[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() != ".pdf":
            continue
        try:
            relative_parts = path.relative_to(ROOT).parts
        except ValueError:
            continue
        if any(part.startswith(".") for part in relative_parts):
            continue
        destination_dir = pick_destination(path, case_map)
        if destination_dir in path.parents and path.parent == destination_dir:
            continue
        dest_path = destination_dir / path.name
        if dest_path == path:
            continue
        ensure_directory(destination_dir)
        if dest_path.exists():
            try:
                if dest_path.samefile(path):
                    skipped.append(path)
                    continue
            except FileNotFoundError:
                pass
            dest_path = unique_destination(dest_path)
        shutil.move(str(path), dest_path)
        moved.append((path, dest_path))
    print(f"Moved {len(moved)} PDF(s).")
    for src, dest in moved[:20]:
        print(f"  {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
    if len(moved) > 20:
        print(f"  ... and {len(moved) - 20} more")
    if skipped:
        print(f"Skipped {len(skipped)} PDF(s) that already matched destination.")


if __name__ == "__main__":
    main()
