---
name: arxiv-search
description: ArXiv paper search — tool reference, workflows, and report formats
---

# ArXiv Paper Search — Skill

## Tools

| Tool | Purpose |
|------|---------|
| arxiv_search | Search papers by query with field prefixes and Boolean operators |
| arxiv_get_paper | Get full metadata + abstract by ArXiv ID (comma-separated for batch) |
| arxiv_download_paper | Download paper PDF to local directory |

## Search Strategy

### Query Construction

Always use field prefixes for precision:
- `ti:` — title
- `au:` — author
- `abs:` — abstract
- `cat:` — category
- `all:` — all fields

Combine with Boolean operators: `AND`, `OR`, `ANDNOT`

**Phrases:** `ti:"attention mechanism"` (double quotes)

**Date filtering:** `submittedDate:[YYYYMMDD0000 TO YYYYMMDD0000]`

### Query Refinement Strategy

1. Start specific (field prefix + category filter)
2. If too few results → broaden (remove category, use `all:` instead of `ti:`)
3. If too many results → narrow (add `AND`, add category, use date filter)

**Minimum:** 3 query variations per research task (single query misses relevant results).

**Techniques:**
- **Synonyms as separate queries:** "retrieval augmented generation" vs "RAG" vs "knowledge grounded generation"
- **Abstraction levels:** specific ("sparse attention transformer") → broad ("efficient transformers")
- **Category scoping:** `cat:cs.CL AND ti:retrieval` narrows to NLP papers

### Common Categories

| Code | Field |
|------|-------|
| cs.CL | Computation and Language (NLP) |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.AI | Artificial Intelligence |
| cs.IR | Information Retrieval |
| stat.ML | Statistics — Machine Learning |

## Parameter Reference

### arxiv_search

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | str | required | Search query with field prefixes and Boolean operators |
| sort_by | relevance/lastUpdatedDate/submittedDate | relevance | Sort order |
| sort_order | descending/ascending | descending | Sort direction |
| start | int | 0 | Offset for pagination |
| max_results | int | 10 | Number of results to return |

**Output:** Paper list with title, ArXiv ID, authors, date, categories, abstract preview (500 chars).

### arxiv_get_paper

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| ids | str | required | Comma-separated ArXiv IDs (e.g., "2301.12345,2305.67890") |

**Output:** Full metadata per paper: title, all authors, full abstract, DOI, journal ref, comment, categories.

**When to use:** Search results only show 500 char abstract preview. Use get_paper for the full abstract to understand actual contribution.

### arxiv_download_paper

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| arxiv_id | str | required | Single ArXiv ID |
| output_dir | str | required | Directory to save PDF |

**Output:** Confirmation with file path. After download: use `/rag:pdf-convert` from RAG plugin for MD conversion.

**NEVER download without explicit user request.** Ask user for output path if not provided.

## Workflow (MANDATORY)

### Step 1: Search Broadly

Fire 3-5 query variations:
- Rephrase the topic using different terms and field prefixes
- Start specific (`ti:` + category), then broaden (`all:`)
- Try synonyms as separate searches, not combined queries
- Use `sort_by=submittedDate` for recent work, `relevance` for best match

### Step 2: Get Full Details

For the top 5-10 results by relevance:
- Call `arxiv_get_paper` with comma-separated IDs to get full abstracts
- Search results only show 500 char preview — full abstract reveals actual contribution

### Step 3: Synthesize

Report findings in structured format.

## Report Format

**Every finding MUST include ArXiv ID + concrete evidence.**

```
## Findings

### 1. <Title>
**ArXiv ID:** <id>
**Authors:** <first author et al.>
**Date:** <submitted date>
**Category:** <primary category>
**Abstract Summary:** <2-3 sentences capturing actual contribution, not just topic>
**Relevance:** <why this paper matters for the research question>

### 2. <Title>
...

[5-10 results total]

## Search Metadata
**Queries Used:** query1, query2, query3, ...
**Total Results Reviewed:** N
**Papers with Full Abstract Read:** N
```

## Result Limits

- **Search:** Fetch 10-20 results per query, read full abstracts on top 5-10
- **Batch lookup:** Use comma-separated IDs in get_paper for efficiency (one call, multiple papers)
- **Pagination:** Use `start` parameter for additional results (start=0, start=10, start=20)

## Presentation

- Present search results as a summary table when > 5 results
- Highlight the most relevant papers with a brief reason why
- When researching a topic: search first, then get_paper on interesting hits for full abstracts

## Guidelines

- **Iterate searches**: Never give up after one query
- **Read abstracts**: Full abstract via get_paper, not just search previews
- **Be specific**: Include ArXiv IDs for every finding
- **Be honest**: Report if search yields poor results
- **Note dates**: Recent papers > old papers for rapidly evolving topics

## Known Limitations

- **Abstract preview in search is 500 chars** — always use get_paper for full abstract on important results
- **ArXiv API rate limit** — 3 second delay between calls (server handles this)
- **No full-text search** — ArXiv API searches metadata only (title, abstract, authors), not paper body
- **Category codes are strict** — `cs.LG` works, `machine learning` as category does not

## When to Stop

- **Verification task** ("find paper X", "what did author Y publish"): Found the specific answer → STOP immediately.
- **Research task** ("papers about X", "state of the art in Y"): Minimum 3 distinct queries before stopping. Stop when 5-10 high-quality results found.
- After finding papers: switch to READING (get_paper for full abstracts) — no more searching.
