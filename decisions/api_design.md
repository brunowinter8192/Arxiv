# API Design

## Status Quo (IST)

- ArXiv Atom API via `export.arxiv.org/api/query`
- XML response parsed with `feedparser`
- Three access patterns: search (query + sort + pagination), ID lookup (single/multi), PDF download
- Query passed through to ArXiv API without validation or modification
- `MAX_RESULTS=2000` cap in search workflow
- PDF download streams to local filesystem with `iter_content(chunk_size=8192)`

## Evidenz

No benchmarks run. API design follows ArXiv API documentation.

## Recommendation (SOLL)

Pending — needs evaluation.

## Offene Fragen

- Should query validation be added (e.g., ArXiv field prefixes like `au:`, `ti:`)?
- Rate limiting: ArXiv recommends max 1 request per 3 seconds — not currently enforced

## Quellen

None indexed.
