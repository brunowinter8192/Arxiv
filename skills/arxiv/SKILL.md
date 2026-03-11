# ArXiv Skill

## Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `arxiv_search` | Search papers by query | Default entry point for paper discovery |
| `arxiv_get_paper` | Full metadata by ID | When user wants full abstract or details on a specific paper |
| `arxiv_download_paper` | Download PDF | ONLY when user explicitly requests download AND provides output path |

## Tool Usage Rules

### arxiv_search

- Default tool for finding papers
- Always use field prefixes for precision: `ti:`, `au:`, `abs:`, `cat:`, `all:`
- Combine with Boolean operators: `AND`, `OR`, `ANDNOT`
- Default `max_results=10` — increase only when user wants more
- Use `sort_by=submittedDate` for recent papers, `relevance` for best match
- Date filtering: `submittedDate:[YYYYMMDD0000 TO YYYYMMDD0000]`
- Phrases: `ti:"attention mechanism"` (double quotes)
- Category codes: `cs.CL` (NLP), `cs.CV` (Vision), `cs.LG` (ML), `cs.AI` (AI), `cs.IR` (Information Retrieval)

**Query Construction Strategy:**
1. Start specific (field prefix + category filter)
2. If too few results → broaden (remove category, use `all:` instead of `ti:`)
3. If too many results → narrow (add `AND`, add category, use date filter)

### arxiv_get_paper

- Use when user wants the **full abstract** (search only shows 500 char preview)
- Use when user provides a specific ArXiv ID
- Use to get detailed metadata (DOI, journal ref, comment, all authors)
- Supports comma-separated IDs for batch lookup

### arxiv_download_paper

- **NEVER download without explicit user request**
- **NEVER use default path** — always ask user for `output_dir` or use the path they provide
- After download: inform user about `/pdf-convert` from RAG plugin for MD conversion

## Presentation

- Present search results as a summary table when > 5 results
- Highlight the most relevant papers with a brief reason why
- When user asks about a topic: search first, then offer to show full details on interesting hits
