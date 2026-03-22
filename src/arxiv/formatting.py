# INFRASTRUCTURE
import logging

logger = logging.getLogger(__name__)


# FUNCTIONS

def format_paper_list(data: dict) -> str:
    papers = data["papers"]
    if not papers:
        return "No papers found."

    total = data["total_results"]
    start = data["start_index"]
    count = len(papers)

    lines = [f"Found {total} total results (showing {start + 1}-{start + count}):\n"]

    for p in papers:
        lines.append("---")
        lines.append(f"Title: {p['title']}")
        lines.append(f"Authors: {', '.join(p['authors'][:5])}" + (" et al." if len(p['authors']) > 5 else ""))
        lines.append(f"Category: {p['primary_category']} | {', '.join(p['categories'][:3])}")
        lines.append(f"Published: {p['published'][:10]} | Updated: {p['updated'][:10]}")
        lines.append(f"ID: {p['id']}")
        lines.append(f"PDF: {p['pdf_link']}")

        if p["doi"]:
            lines.append(f"DOI: {p['doi']}")
        if p["journal_ref"]:
            lines.append(f"Journal: {p['journal_ref']}")

        abstract = p["summary"]
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."
        lines.append(f"Abstract: {abstract}")
        lines.append("")

    return "\n".join(lines)


def format_paper_detail(data: dict) -> str:
    papers = data["papers"]
    if not papers:
        return "Paper not found."

    lines = []
    for p in papers:
        lines.append("===")
        lines.append(f"Title: {p['title']}")
        lines.append(f"Authors: {', '.join(p['authors'])}")
        lines.append(f"Category: {p['primary_category']} | All: {', '.join(p['categories'])}")
        lines.append(f"Published: {p['published']}")
        lines.append(f"Updated: {p['updated']}")
        lines.append(f"ID: {p['id']}")
        lines.append(f"PDF: {p['pdf_link']}")
        lines.append(f"Abstract Page: {p['abstract_link']}")

        if p["doi"]:
            lines.append(f"DOI: {p['doi']}")
        if p["journal_ref"]:
            lines.append(f"Journal: {p['journal_ref']}")
        if p["comment"]:
            lines.append(f"Comment: {p['comment']}")

        lines.append(f"\nAbstract:\n{p['summary']}")
        lines.append("")

    return "\n".join(lines)
