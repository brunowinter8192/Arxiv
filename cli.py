#!/usr/bin/env python3
import os
import sys

# Ensure src.arxiv.* imports resolve regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse

from src.arxiv.search import search_workflow
from src.arxiv.get_paper import get_paper_workflow
from src.arxiv.download_paper import download_paper_workflow


def main():
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="ArXiv CLI — search papers, get metadata, and download PDFs."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ── search ────────────────────────────────────────────────────────────────
    p = sub.add_parser("search", help="Search ArXiv papers.")
    p.add_argument("query", help="Search query with field prefixes (e.g. 'ti:attention AND cat:cs.CL')")
    p.add_argument("--sort-by", dest="sort_by",
                   choices=["relevance", "lastUpdatedDate", "submittedDate"],
                   default="relevance")
    p.add_argument("--sort-order", dest="sort_order",
                   choices=["descending", "ascending"],
                   default="descending")
    p.add_argument("--start", type=int, default=0, help="Offset for pagination")
    p.add_argument("--max-results", dest="max_results", type=int, default=10,
                   help="Number of results to return (max 2000)")

    # ── get_paper ─────────────────────────────────────────────────────────────
    p = sub.add_parser("get_paper", help="Get full metadata by ArXiv ID.")
    p.add_argument("ids", help="Comma-separated ArXiv IDs (e.g. '2301.12345,2305.67890')")

    # ── download_paper ────────────────────────────────────────────────────────
    p = sub.add_parser("download_paper", help="Download paper PDF to local directory.")
    p.add_argument("arxiv_id", help="Single ArXiv ID (e.g. '2301.12345')")
    p.add_argument("output_dir", help="Directory to save the PDF")

    # ── Dispatch ──────────────────────────────────────────────────────────────
    args = parser.parse_args()

    if args.cmd == "search":
        result = search_workflow(args.query, args.sort_by, args.sort_order, args.start, args.max_results)

    elif args.cmd == "get_paper":
        result = get_paper_workflow(args.ids)

    elif args.cmd == "download_paper":
        result = download_paper_workflow(args.arxiv_id, args.output_dir)

    else:
        parser.error(f"Unknown command: {args.cmd}")

    print(result[0].text)


if __name__ == "__main__":
    main()
