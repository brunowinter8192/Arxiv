# ArXiv MCP Server

Search and retrieve academic papers from ArXiv.

## Sources

See [sources/sources.md](sources/sources.md).

## Pipeline Components

### API Layer

| Component | Implementation | Config |
|-----------|---------------|--------|
| **ArXiv API** | `src/arxiv/search.py`, `src/arxiv/get_paper.py`, `src/arxiv/download_paper.py` | Atom/XML feed via `export.arxiv.org`, `MAX_RESULTS=2000` cap |
| **XML Parsing** | `src/arxiv/parsing.py` — feedparser-based Atom parsing | Extracts metadata, categories, links, DOI |
| **Formatting** | `src/arxiv/formatting.py` — list view (truncated abstracts) + detail view (full) | Abstract truncation at 500 chars in list view |

### Delivery

| Component | Implementation | Config |
|-----------|---------------|--------|
| **MCP Server** | `server.py` via FastMCP | 3 tools (search, get_paper, download_paper) |

### Key Files

| File | Purpose |
|------|---------|
| `server.py` | MCP server — tool definitions, delegates to src/arxiv/ |
| `src/arxiv/parsing.py` | Shared XML parsing + API base URL |
| `src/arxiv/formatting.py` | Output formatting (list + detail views) |
| `src/arxiv/DOCS.md` | Tool reference documentation |

## Project Structure

```
arxiv/
├── server.py
├── requirements.txt
├── README.md                       → [Setup & External Docs](README.md)
├── decisions/
├── src/
│   └── arxiv/                      → [DOCS.md](src/arxiv/DOCS.md)
```
