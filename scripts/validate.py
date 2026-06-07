#!/usr/bin/env python3
"""Validate plugin manifests and skill frontmatter. Run locally or in CI.

Checks:
  - Every plugin manifest JSON parses and has a `name`.
  - Every skills/<dir>/SKILL.md has YAML frontmatter with `name` and
    `description`, the `name` matches its directory, uses only [a-z0-9-],
    and the frontmatter block is <= 1024 characters.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors: list[str] = []

MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
]

for rel in MANIFESTS:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"{rel}: missing")
        continue
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{rel}: invalid JSON ({exc})")
        continue
    if "marketplace" in rel:
        if not isinstance(data.get("plugins"), list) or not data["plugins"]:
            errors.append(f"{rel}: `plugins` must be a non-empty array")
    elif not data.get("name"):
        errors.append(f"{rel}: missing `name`")

NAME_RE = re.compile(r"^[a-z0-9-]+$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

skills_dir = ROOT / "skills"
skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.exists() else []
if not skill_files:
    errors.append("skills/: no SKILL.md files found")

for skill in skill_files:
    text = skill.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append(f"{skill.relative_to(ROOT)}: missing `---` YAML frontmatter")
        continue
    block = m.group(1)
    if len(block) > 1024:
        errors.append(f"{skill.relative_to(ROOT)}: frontmatter exceeds 1024 chars")
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    name = fields.get("name", "")
    if not name:
        errors.append(f"{skill.relative_to(ROOT)}: frontmatter missing `name`")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{skill.relative_to(ROOT)}: name `{name}` must match [a-z0-9-]")
        if name != skill.parent.name:
            errors.append(
                f"{skill.relative_to(ROOT)}: name `{name}` != directory `{skill.parent.name}`"
            )
    if not fields.get("description"):
        errors.append(f"{skill.relative_to(ROOT)}: frontmatter missing `description`")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: {len(MANIFESTS)} manifests, {len(skill_files)} skills validated.")
