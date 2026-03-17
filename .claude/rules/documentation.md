---
paths:
  - "**/*.md"
  - "**/DOCS.md"
  - "**/README.md"
---

# Documentation Hierarchy

Three documentation layers, each with distinct audience and scope.

## CLAUDE.md (Root)

**Audience:** AI (Claude Code sessions).
**Purpose:** Maps root level for AI navigation. Contains project overview, pipeline components, key files, startup instructions.
**Scope:** Root-level structure. References `data/` and `decisions/` with their purpose. Links to DOCS.md for module details.

**Not a substitute for DOCS.md.** CLAUDE.md provides orientation; DOCS.md provides module documentation.

## README.md (Root)

**Audience:** External user (human).
**Purpose:** Setup, installation, how to use, what is this project.
**Scope:** Only documents the level it lives on. Tree shows root-level files only.

**Required Sections:**
1. Title + one-liner description
2. Directory tree (root-level only, link to DOCS.md)
3. Setup / Installation
4. Environment Variables (if applicable)

**Rule:** README stops where DOCS begins. No redundancy.

## DOCS.md

**Audience:** Developer (human or AI).
**Purpose:** Module documentation on the level it lives on.

### Placement Rules

1. **Directory with multiple modules (.py/.sh files)** → DOCS.md lives IN that directory
2. **Directory with single module** → Documented in PARENT directory's DOCS.md (no own DOCS.md)
3. **Hub directories** (directories that only contain subdirectories, no direct modules) → DOCS.md with purpose description + Documentation Tree only
4. **Tightly coupled submodules** (e.g., `retrievers/` inside `eval/`) → Documented in parent DOCS.md, no own DOCS.md. Applies when the subdir is a package of the parent module, not an independent suite.

### Documentation Tree (when sub-DOCS exist)

DOCS.md files that have darunterliegende DOCS MUST include a tree section mapping to them:

```markdown
## Documentation Tree

- [path/to/DOCS.md](path/to/DOCS.md) — One-line description
```

**Rules:**
- Only map the NEXT level of DOCS, not deeper levels
- If a subdirectory has no own DOCS.md (single-file, documented in current DOCS), it does NOT appear in the tree
- The tree is the navigation structure for AI and developers

### Module Documentation Format

```markdown
## module_name.py

**Purpose:** What this module does.
**Input:** What it takes.
**Output:** What it returns.
```

**Rules:**
- NO function-level documentation (only Purpose/Input/Output)
- Describe WHAT not HOW
- Include Usage examples for scripts (how to run from project root)
- Include CLI flags table for scripts with argparse

### Directories That Do NOT Need DOCS

| Directory | Reason |
|---|---|
| `agents/`, `commands/`, `skills/` | Plugin structure (Claude Code convention) |
| `data/` | Data storage, purpose documented in CLAUDE.md |
| `decisions/` | IS documentation (pipeline decision records) |
| `.claude/`, `.claude-plugin/` | Tool configuration |

### dev/ Suites

dev/ directories follow the same placement rules. Single-script suites are documented in their parent DOCS.md. Multi-script suites get their own DOCS.md.

**Format for dev/ modules:**
- Purpose of the script/suite
- Usage examples (how to run from project root)
- CLI flags if applicable
- Expected output description
