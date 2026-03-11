# INFRASTRUCTURE
import feedparser


API_BASE = "http://export.arxiv.org/api/query"


# FUNCTIONS

def parse_feed(xml_text: str) -> dict:
    feed = feedparser.parse(xml_text)
    total_results = int(feed.feed.get("opensearch_totalresults", 0))
    start_index = int(feed.feed.get("opensearch_startindex", 0))
    items_per_page = int(feed.feed.get("opensearch_itemsperpage", 0))

    papers = [parse_entry(entry) for entry in feed.entries if not is_error_entry(entry)]

    return {
        "total_results": total_results,
        "start_index": start_index,
        "items_per_page": items_per_page,
        "papers": papers,
    }


def is_error_entry(entry) -> bool:
    return entry.get("title", "") == "Error"


def parse_entry(entry) -> dict:
    arxiv_id = entry.get("id", "").replace("http://arxiv.org/abs/", "")

    authors = [a.get("name", "") for a in entry.get("authors", [])]

    categories = [t.get("term", "") for t in entry.get("tags", [])]

    primary_category = ""
    if hasattr(entry, "arxiv_primary_category"):
        primary_category = entry.arxiv_primary_category.get("term", "")

    pdf_link = ""
    abstract_link = ""
    for link in entry.get("links", []):
        if link.get("title") == "pdf":
            pdf_link = link.get("href", "")
        if link.get("rel") == "alternate":
            abstract_link = link.get("href", "")

    return {
        "id": arxiv_id,
        "title": clean_text(entry.get("title", "")),
        "summary": clean_text(entry.get("summary", "")),
        "authors": authors,
        "categories": categories,
        "primary_category": primary_category,
        "published": entry.get("published", ""),
        "updated": entry.get("updated", ""),
        "pdf_link": pdf_link,
        "abstract_link": abstract_link,
        "doi": getattr(entry, "arxiv_doi", ""),
        "journal_ref": getattr(entry, "arxiv_journal_ref", ""),
        "comment": clean_text(getattr(entry, "arxiv_comment", "") or ""),
    }


def clean_text(text: str) -> str:
    return " ".join(text.split())
