# CLAUDE.MD - ArXiv MCP Server Engineering Reference

## PROJECT

- **GitHub Repo:** `brunowinter8192/arxiv`
- **Bugs:** GitHub Issues (`gh issue create --repo brunowinter8192/arxiv`)

### Sources
- **ArXiv API:** https://info.arxiv.org/help/api/index.html (query syntax, field prefixes, rate limits)
- **ArXiv API User Manual:** https://info.arxiv.org/help/api/user-manual.html (search parameters, paging, sorting)
- **FastMCP:** https://github.com/PrefectHQ/fastmcp (MCP server framework)
- **feedparser:** https://feedparser.readthedocs.io/ (Atom feed parsing)

Consult these sources before making assumptions about API behavior or query syntax.

---

## CRITICAL STANDARDS

- NO comments inside function bodies (only function header comments + section markers)
- NO test files in root (ONLY in debug/ folders)
- NO debug/ or logs/ folders in version control (MUST be in .gitignore)

**Fail-Fast:** Let exceptions fly. `requests.raise_for_status()` on every API call. No try-catch that silently swallows errors.

---

## General

- NO emojis in production code, READMEs, DOCS.md, logs
- ALWAYS keep script console output concise

For system configuration and parameter details: **See README.md**

### Testing

**CRITICAL:** Test MCP tools by calling them directly via MCP tool calls, NOT via Python import.

**RIGHT:**
```
mcp__plugin_arxiv_arxiv__arxiv_search(query="ti:test", max_results=1)
```

**WRONG:**
```bash
source .venv/bin/activate && python -c "from src.arxiv.search import ..."
```

**Rules:**
- The MCP server runs as a separate process - there is no local venv to activate
- Always use `mcp__plugin_arxiv_arxiv__<tool_name>(...)` to verify tool behavior
- **After code changes:** MCP server must be restarted before tool calls reflect changes. Ask user to restart (`/mcp` in Claude Code) before running verification tests

---

## server.py (MCP Entry Point)

**Purpose:** MCP server exposing tools to Claude Code. Only imports and tool definitions.

```python
# INFRASTRUCTURE
from typing import Annotated, Literal
from fastmcp import FastMCP
from pydantic import Field
from mcp.types import TextContent

from src.arxiv.search import search_workflow

mcp = FastMCP("ArXiv")


# TOOLS

@mcp.tool
def arxiv_search(
    query: Annotated[str, Field(description="Search query using ArXiv syntax...")],
    max_results: Annotated[int, Field(description="Max results (1-2000)")] = 10,
) -> list[TextContent]:
    """Search ArXiv papers by query. Use field prefixes..."""
    return search_workflow(query, max_results=max_results)
```

**Rules:**
- NO business logic in server.py
- Each tool delegates to module orchestrator
- All parameters use Annotated + Field
- Literal for enum-like choices with clear descriptions
- Return type: `list[TextContent]` (MCP standard)

---

## MODULE PATTERN (src/arxiv/module_name.py)

**CRITICAL:** Each module follows INFRASTRUCTURE -> ORCHESTRATOR -> FUNCTIONS

```python
# INFRASTRUCTURE
import requests
from mcp.types import TextContent

from src.arxiv.parsing import API_BASE, parse_feed


# ORCHESTRATOR
def search_workflow(query: str, ...) -> list[TextContent]:
    raw_xml = fetch_search(query, ...)
    data = parse_feed(raw_xml)
    formatted = format_paper_list(data)
    return [TextContent(type="text", text=formatted)]


# FUNCTIONS

def fetch_search(query: str, ...) -> str:
    ...
```

**Section definitions:**

**INFRASTRUCTURE:**
- Imports and constants
- NO functions, NO logic

**ORCHESTRATOR:**
- ONE function (named: `tool_name_workflow`)
- Called by server.py tool definition
- Calls internal functions in sequence
- ZERO functional logic (only function composition)

**FUNCTIONS:**
- Ordered by call sequence
- One responsibility each
- Function header comment (one line describing WHAT)
- NO inline comments

**Shared modules** (parsing.py, formatting.py) may have only INFRASTRUCTURE + FUNCTIONS (no ORCHESTRATOR) when they serve as utility modules called by other orchestrators.

---

## TOOL PARAMETER DESIGN

**CRITICAL:** Parameters must be intuitive for LLM understanding

### Two-Layer Documentation (NO DUPLICATION)

**Field Description** = Technical parameter details (what, how, format)
**Docstring** = Semantic use cases (when, why to use this tool)

**Field tells LLM:** "How do I fill this parameter?"
**Docstring tells LLM:** "When should I call this tool?"

---

## ERROR HANDLING

**IMPORTANT:** Fail-fast philosophy

- `requests.raise_for_status()` on every HTTP call
- FastMCP handles exceptions and communicates errors to client
- No silent error swallowing
- Explicit early returns for "not found" cases (e.g., no papers, no PDF link)

---

## DOCUMENTATION STRUCTURE

### Hierarchy

```
arxiv/             -> README.md (setup, tools, query syntax)
  src/arxiv/       -> DOCS.md (module-level docs)
```

**Principle:** README stops where DOCS begins. No redundancy.

### README Content

README.md contains:
- Quick start / usage
- MCP tool reference with parameter tables
- Directory structure (tree)
- ArXiv query syntax reference
- Links to DOCS.md for module details

---

## NAMING CONVENTIONS

**server.py:** Always named server.py
**Domain folders:** src/arxiv/ (snake_case)
**Modules:** src/arxiv/search.py, src/arxiv/parsing.py
**Package markers:** src/__init__.py and src/arxiv/__init__.py (required for imports)
**Orchestrator function:** tool_name_workflow()
**MCP tool function:** @mcp.tool def arxiv_tool_name()

---

## COMPLIANCE

Scripts in `debug/` folders are exempt from CLAUDE.md compliance requirements.

All other code must follow these standards strictly.
