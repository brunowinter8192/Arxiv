# ArXiv MCP Plugin

Search, retrieve, and download academic papers from ArXiv directly in Claude Code.

## Features

- **Paper search** — query by title, author, abstract, category with Boolean operators
- **Paper metadata** — full details: authors, abstract, categories, DOI, links
- **PDF download** — save papers locally for reading or indexing
- **Autonomous research agent** — dispatches `arxiv-search` for multi-step literature reviews

## Quick Start

```
/plugin marketplace add brunowinter8192/claude-plugins
/plugin install arxiv
```

Restart the session after installation. The plugin is ready to use — no API keys required.

## Prerequisites

- Python >= 3.10
- Internet connection (ArXiv API is public and free, no auth required)

## Setup

For manual installation without the plugin marketplace:

```bash
git clone https://github.com/brunowinter8192/Arxiv.git
cd Arxiv
python -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

Add to your project's `.mcp.json` (absolute paths):

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "/absolute/path/to/Arxiv/mcp-start.sh",
      "args": []
    }
  }
}
```

`mcp-start.sh` auto-creates the venv if missing.

## Usage

### MCP Tools

| Tool | What it does | When to use |
|------|-------------|-------------|
| `arxiv_search` | Search papers by query with field prefixes and Boolean operators | Finding papers on a topic, exploring recent work |
| `arxiv_get_paper` | Retrieve full metadata for one or more papers by ArXiv ID | Looking up a specific paper, getting full abstract and links |
| `arxiv_download_paper` | Download a paper's PDF to a local directory | Saving papers for offline reading or RAG indexing |

#### Query Syntax

| Prefix | Field | Example |
|--------|-------|---------|
| `ti:` | Title | `ti:transformer` |
| `au:` | Author | `au:bengio` |
| `abs:` | Abstract | `abs:"reinforcement learning"` |
| `cat:` | Category | `cat:cs.CL` |
| `all:` | All fields | `all:attention` |

Boolean operators: `AND`, `OR`, `ANDNOT` (uppercase). Date filter: `submittedDate:[YYYYMMDD0000 TO YYYYMMDD0000]`.

### Skills & Commands

| Skill | What it does |
|-------|-------------|
| `/arxiv:agent-arxiv-search` | Tool reference and query strategy guide for the arxiv-search agent |

### Agents

| Agent | What it handles |
|-------|----------------|
| `arxiv-search` | Autonomous paper search specialist — multi-step literature review, query refinement, result summarization |

## Workflows

**Literature review:** Ask Claude to research a topic. The `arxiv-search` agent runs multiple queries with different field prefixes, filters by category and date, and returns a curated paper list with summaries.

**Paper lookup + download:** Use `arxiv_get_paper` to fetch metadata for known ArXiv IDs, then `arxiv_download_paper` to save PDFs locally.

**Exploratory search:** Start broad with `all:keyword`, then narrow with `ti:` and `cat:` prefixes once you know the relevant categories.

## Troubleshooting

<details>
<summary>No results returned</summary>

ArXiv search is exact-match on field prefixes. Try:
- Use `all:keyword` instead of a bare query
- Check Boolean operators are uppercase (`AND`, not `and`)
- Remove date filters to broaden the search
- Simplify the query — fewer conditions return more results
</details>

<details>
<summary>ArXiv API rate limiting</summary>

ArXiv recommends at least 3 seconds between requests. If you receive empty responses or connection errors after rapid successive searches, wait a few seconds before retrying. The plugin does not add automatic delays.
</details>

<details>
<summary>PDF download fails or saves to wrong path</summary>

- `output_dir` must be an absolute path that exists on your filesystem (e.g., `/tmp/papers`)
- If the directory does not exist, create it first: `mkdir -p /tmp/papers`
- Check that the ArXiv ID is valid — use `arxiv_get_paper` first to confirm the paper exists
</details>

## License

MIT
