# src/arxiv/ - ArXiv API Modules

## Directory Structure

```
src/arxiv/
  __init__.py
  parsing.py           # XML feed parsing + data extraction
  search.py            # Search orchestration
  get_paper.py         # Paper metadata retrieval by ID
  download_paper.py    # PDF download
  formatting.py        # Output formatting (list + detail views)
```

---

## parsing.py

**Purpose:** Parse ArXiv Atom XML feeds into structured Python dicts.

**Input:** Raw XML text from ArXiv API
**Output:** Dict with `total_results`, `start_index`, `items_per_page`, `papers` list

**Usage:**
```python
from src.arxiv.parsing import API_BASE, parse_feed

data = parse_feed(xml_text)
papers = data["papers"]  # list[dict]
```

**Constants:**
| Constant | Value | Description |
|----------|-------|-------------|
| API_BASE | `http://export.arxiv.org/api/query` | ArXiv API endpoint |

**Functions:**
| Function | Purpose |
|----------|---------|
| `parse_feed(xml_text)` | Parse XML into structured dict with metadata + paper list |
| `is_error_entry(entry)` | Check if feed entry is an error response |
| `parse_entry(entry)` | Extract paper fields from a single feed entry |
| `clean_text(text)` | Normalize whitespace in text fields |

**Paper dict fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | str | ArXiv ID (e.g., `2301.07041v1`) |
| `title` | str | Paper title (whitespace-normalized) |
| `summary` | str | Full abstract |
| `authors` | list[str] | Author names |
| `categories` | list[str] | All category tags |
| `primary_category` | str | Primary category |
| `published` | str | Publication date (ISO format) |
| `updated` | str | Last update date (ISO format) |
| `pdf_link` | str | Direct PDF URL |
| `abstract_link` | str | Abstract page URL |
| `doi` | str | DOI (if available) |
| `journal_ref` | str | Journal reference (if available) |
| `comment` | str | Author comment (if available) |

---

## search.py

**Purpose:** Orchestrate ArXiv search queries.

**Input:** Query string, sort parameters, pagination
**Output:** `list[TextContent]` with formatted search results

**Usage:**
```python
from src.arxiv.search import search_workflow

results = search_workflow("ti:transformer AND cat:cs.CL", max_results=5)
```

**Constants:**
| Constant | Value | Description |
|----------|-------|-------------|
| MAX_RESULTS | 2000 | Hard cap on results per query |

**Functions:**
| Function | Purpose |
|----------|---------|
| `search_workflow(query, sort_by, sort_order, start, max_results)` | Orchestrator: fetch, parse, format |
| `fetch_search(query, sort_by, sort_order, start, max_results)` | HTTP GET to ArXiv API with search params |

---

## get_paper.py

**Purpose:** Retrieve full metadata for papers by ArXiv ID.

**Input:** Comma-separated ArXiv IDs
**Output:** `list[TextContent]` with detailed paper metadata

**Usage:**
```python
from src.arxiv.get_paper import get_paper_workflow

details = get_paper_workflow("2301.07041,2305.14314")
```

**Functions:**
| Function | Purpose |
|----------|---------|
| `get_paper_workflow(ids)` | Orchestrator: fetch by ID, parse, format detail view |
| `fetch_by_ids(ids)` | HTTP GET to ArXiv API with id_list param |

---

## download_paper.py

**Purpose:** Download paper PDFs from ArXiv.

**Input:** ArXiv ID, output directory
**Output:** `list[TextContent]` with download status (path, title, authors)

**Usage:**
```python
from src.arxiv.download_paper import download_paper_workflow

result = download_paper_workflow("2301.07041", "/tmp/papers")
```

**Functions:**
| Function | Purpose |
|----------|---------|
| `download_paper_workflow(arxiv_id, output_dir)` | Orchestrator: fetch metadata, download PDF, return status |
| `fetch_by_id(arxiv_id)` | HTTP GET to ArXiv API for single paper metadata |
| `download_pdf(url, filepath)` | Stream-download PDF to local file |

---

## formatting.py

**Purpose:** Format parsed paper data into human-readable text output.

**Input:** Parsed data dict from `parse_feed()`
**Output:** Formatted string

**Usage:**
```python
from src.arxiv.formatting import format_paper_list, format_paper_detail

text = format_paper_list(data)    # Search results (truncated abstract, max 500 chars)
text = format_paper_detail(data)  # Full detail view (complete abstract)
```

**Functions:**
| Function | Purpose |
|----------|---------|
| `format_paper_list(data)` | Format search results: truncated abstract (500 chars), top 5 authors |
| `format_paper_detail(data)` | Format full detail: complete abstract, all authors, all metadata |
