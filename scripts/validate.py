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
    ".cursor-plugin/marketplace.json",
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

# Claude manifest contract (per code.claude.com/docs/en/plugins-reference + plugin-marketplaces).
# Claude ignores unrecognized fields, so only enforce required shape + load-error cases.
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
clp = ROOT / ".claude-plugin" / "plugin.json"
clp_name = None
if clp.exists():
    try:
        cl = json.loads(clp.read_text())
    except json.JSONDecodeError:
        cl = None
    if cl is not None:
        clp_name = cl.get("name")
        if not KEBAB_RE.match(str(cl.get("name", ""))):
            errors.append(".claude-plugin/plugin.json: `name` is required and must be kebab-case")
        if "keywords" in cl and not (isinstance(cl["keywords"], list) and all(isinstance(k, str) for k in cl["keywords"])):
            errors.append(".claude-plugin/plugin.json: `keywords` must be an array of strings (wrong type is a load error)")

clm = ROOT / ".claude-plugin" / "marketplace.json"
if clm.exists():
    try:
        cmk = json.loads(clm.read_text())
    except json.JSONDecodeError:
        cmk = None
    if cmk is not None:
        if not KEBAB_RE.match(str(cmk.get("name", ""))):
            errors.append(".claude-plugin/marketplace.json: `name` is required and must be kebab-case")
        if not str((cmk.get("owner") or {}).get("name", "")).strip():
            errors.append(".claude-plugin/marketplace.json: `owner.name` is required")
        for e in cmk.get("plugins") or []:
            if not e.get("name") or not e.get("source"):
                errors.append(".claude-plugin/marketplace.json: each plugin entry needs `name` and `source`")

# Codex manifest contract (subset of openai/codex plugin-json-spec validator).
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+].+)?$")
codex = ROOT / ".codex-plugin" / "plugin.json"
if codex.exists():
    try:
        cx = json.loads(codex.read_text())
    except json.JSONDecodeError:
        cx = None
    if cx is not None:
        allowed_top = {"id", "name", "version", "description", "skills", "apps",
                       "mcpServers", "interface", "author", "homepage", "repository",
                       "license", "keywords"}
        for k in set(cx) - allowed_top:
            errors.append(f".codex-plugin/plugin.json: field `{k}` is not accepted (rejects `hooks`/unknown)")
        if not SEMVER_RE.match(str(cx.get("version", ""))):
            errors.append(".codex-plugin/plugin.json: `version` must be strict semver")
        for f in ("name", "description"):
            if not str(cx.get(f, "")).strip():
                errors.append(f".codex-plugin/plugin.json: `{f}` must be a non-empty string")
        if not str((cx.get("author") or {}).get("name", "")).strip():
            errors.append(".codex-plugin/plugin.json: `author.name` is required")
        iface = cx.get("interface") or {}
        for f in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            if not str(iface.get(f, "")).strip():
                errors.append(f".codex-plugin/plugin.json: `interface.{f}` must be a non-empty string")
        caps = iface.get("capabilities")
        if not isinstance(caps, list) or not all(isinstance(c, str) and c.strip() for c in caps):
            errors.append(".codex-plugin/plugin.json: `interface.capabilities` must be a string array")
        if "defaultPrompt" not in iface and "default_prompt" not in iface:
            errors.append(".codex-plugin/plugin.json: `interface.defaultPrompt` is required")

# Cursor manifest contract (subset of cursor/plugins schemas/*.schema.json).
CURSOR_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$")
cur = ROOT / ".cursor-plugin" / "plugin.json"
cur_name = None
if cur.exists():
    try:
        cp = json.loads(cur.read_text())
    except json.JSONDecodeError:
        cp = None
    if cp is not None:
        cur_name = cp.get("name")
        allowed = {"name", "displayName", "description", "version", "author", "publisher",
                   "homepage", "repository", "license", "logo", "keywords", "category",
                   "tags", "commands", "agents", "skills", "rules", "hooks", "mcpServers"}
        for k in set(cp) - allowed:
            errors.append(f".cursor-plugin/plugin.json: field `{k}` is not accepted (schema is additionalProperties:false)")
        if not CURSOR_NAME_RE.match(str(cp.get("name", ""))):
            errors.append(".cursor-plugin/plugin.json: `name` is required and must be kebab-case")
        if "author" in cp:
            a = cp["author"]
            if not isinstance(a, dict) or set(a) - {"name", "email"}:
                errors.append(".cursor-plugin/plugin.json: `author` allows only `name`/`email`")
            elif not str(a.get("name", "")).strip():
                errors.append(".cursor-plugin/plugin.json: `author.name` must be non-empty")

cmp_ = ROOT / ".cursor-plugin" / "marketplace.json"
if cmp_.exists():
    try:
        cm = json.loads(cmp_.read_text())
    except json.JSONDecodeError:
        cm = None
    if cm is not None:
        for k in set(cm) - {"name", "owner", "metadata", "plugins"}:
            errors.append(f".cursor-plugin/marketplace.json: field `{k}` is not accepted")
        if not str(cm.get("name", "")).strip():
            errors.append(".cursor-plugin/marketplace.json: `name` is required")
        entries = cm.get("plugins")
        if not isinstance(entries, list) or not entries:
            errors.append(".cursor-plugin/marketplace.json: `plugins` must be a non-empty array")
        else:
            for e in entries:
                if set(e) - {"name", "source", "description"}:
                    errors.append(".cursor-plugin/marketplace.json: plugin entry has unsupported keys")
                if not e.get("name") or not e.get("source"):
                    errors.append(".cursor-plugin/marketplace.json: each plugin entry needs `name` and `source`")
                if e.get("source") == "." and cur_name and e.get("name") != cur_name:
                    errors.append(f".cursor-plugin/marketplace.json: entry name `{e.get('name')}` must match plugin.json name `{cur_name}`")

# Bundled MCP server config files (optional). When present they auto-configure
# the SenderKit MCP server on plugin install, so keep them parseable and
# well-formed. `.mcp.json` is the Claude Code default (OAuth); Codex points its
# manifest `mcpServers` path at `.codex-plugin/mcp.json` (also OAuth — `url` only);
# Cursor inlines `mcpServers` in its plugin manifest (OAuth, `url` only). All ship
# OAuth-only with no committed credential; API keys are an opt-in per user.
for rel in (".mcp.json", ".codex-plugin/mcp.json"):
    mcp_path = ROOT / rel
    if not mcp_path.exists():
        continue
    try:
        mcp = json.loads(mcp_path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{rel}: invalid JSON ({exc})")
        continue
    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        errors.append(f"{rel}: `mcpServers` must be a non-empty object")
        continue
    for sname, scfg in servers.items():
        if not isinstance(scfg, dict):
            errors.append(f"{rel}: server `{sname}` must be an object")
            continue
        # Remote (url) or local (command) — require one of them.
        if not scfg.get("url") and not scfg.get("command"):
            errors.append(f"{rel}: server `{sname}` needs a `url` or `command`")

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
