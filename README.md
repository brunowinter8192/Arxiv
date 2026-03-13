# ArXiv MCP Server

Search, browse, and download academic papers from ArXiv via MCP for Claude Code.

## Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| API | ArXiv REST API | Official, free, no auth required |
| Feed Parsing | feedparser | Robust Atom/RSS parser, handles ArXiv extensions |
| MCP Framework | FastMCP | Consistent with other MCP servers |

## Installation

### As Plugin (recommended)

In a Claude Code session:

```
/plugin marketplace add brunowinter8192/claude-plugins
/plugin install arxiv
```

Restart the session after installation.

### Manual (.mcp.json)

Add to your project's `.mcp.json` (all paths must be absolute):

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "/absolute/path/to/arxiv/mcp-start.sh",
      "args": []
    }
  }
}
```

## Plugin Components

| Component | Name | Description |
|-----------|------|-------------|
| **Skill** | `/arxiv` | Query construction strategy, field prefixes, presentation rules |
| **MCP Server** | `arxiv` | 3 tools: search, get paper metadata, download PDF |

## MCP Tools

### arxiv_search

Search ArXiv papers by query with field prefixes and Boolean operators.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query using ArXiv syntax (field prefixes + Boolean) |
| `sort_by` | string | No | relevance | `relevance`, `lastUpdatedDate`, or `submittedDate` |
| `sort_order` | string | No | descending | `descending` or `ascending` |
| `start` | int | No | 0 | 0-based index of first result (for paging) |
| `max_results` | int | No | 10 | Max results to return (1-2000) |

```
mcp__plugin_arxiv_arxiv__arxiv_search(query="ti:transformer AND cat:cs.CL", max_results=5)
mcp__plugin_arxiv_arxiv__arxiv_search(query="au:bengio AND submittedDate:[202401010000 TO 202501010000]", sort_by="submittedDate")
```

### arxiv_get_paper

Get full metadata for one or more papers by ArXiv ID.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ids` | string | Yes | Comma-separated ArXiv IDs (e.g., `2301.07041` or `2301.07041,2305.14314`) |

```
mcp__plugin_arxiv_arxiv__arxiv_get_paper(ids="2301.07041")
mcp__plugin_arxiv_arxiv__arxiv_get_paper(ids="2301.07041,2305.14314")
```

### arxiv_download_paper

Download a paper's PDF from ArXiv.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `arxiv_id` | string | Yes | - | ArXiv paper ID (e.g., `2301.07041`) |
| `output_dir` | string | No | /tmp/arxiv | Directory to save the PDF |

```
mcp__plugin_arxiv_arxiv__arxiv_download_paper(arxiv_id="2301.07041", output_dir="/tmp/papers")
```

## Prerequisites

- Python >= 3.10
- Internet connection (ArXiv API is public, no auth required)

## Setup

```bash
git clone https://github.com/brunowinter8192/arxiv.git
cd arxiv
python -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

The `mcp-start.sh` script auto-creates the venv if missing.

## Directory Structure

```
arxiv/
  .claude-plugin/          # Plugin manifest (plugin.json only)
  skills/arxiv/            # Plugin skill (SKILL.md)
  server.py                # MCP Entry Point (Claude Code)
  mcp-start.sh             # Venv bootstrap + server start
  requirements.txt         # Python dependencies
  src/arxiv/               # Module implementations (see DOCS.md)
    parsing.py             # XML feed parsing
    search.py              # Search orchestration
    get_paper.py           # Paper metadata retrieval
    download_paper.py      # PDF download
    formatting.py          # Output formatting
```

**Module details:** [src/arxiv/DOCS.md](src/arxiv/DOCS.md)

## ArXiv Query Syntax

### Field Prefixes

| Prefix | Field | Example |
|--------|-------|---------|
| `ti:` | Title | `ti:transformer` |
| `au:` | Author | `au:bengio` |
| `abs:` | Abstract | `abs:"reinforcement learning"` |
| `cat:` | Category | `cat:cs.CL` |
| `all:` | All fields | `all:attention` |

### Boolean Operators

`AND`, `OR`, `ANDNOT` — must be uppercase.

```
ti:transformer AND cat:cs.CL
au:lecun OR au:bengio
ti:attention ANDNOT cat:cs.CV
```

### Date Filtering

```
submittedDate:[YYYYMMDD0000 TO YYYYMMDD0000]
```

Example: Papers from 2024:
```
au:smith AND submittedDate:[202401010000 TO 202501010000]
```

### Common Categories

| Code | Field |
|------|-------|
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.LG` | Machine Learning |
| `cs.AI` | Artificial Intelligence |
| `cs.IR` | Information Retrieval |
| `stat.ML` | Statistics - Machine Learning |
