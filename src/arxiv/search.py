# INFRASTRUCTURE
import requests
from mcp.types import TextContent

from src.arxiv.parsing import API_BASE, parse_feed
from src.arxiv.formatting import format_paper_list

MAX_RESULTS = 2000


# ORCHESTRATOR
def search_workflow(
    query: str,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    start: int = 0,
    max_results: int = 10,
) -> list[TextContent]:
    raw_xml = fetch_search(query, sort_by, sort_order, start, min(max_results, MAX_RESULTS))
    data = parse_feed(raw_xml)
    formatted = format_paper_list(data)
    return [TextContent(type="text", text=formatted)]


# FUNCTIONS

def fetch_search(query: str, sort_by: str, sort_order: str, start: int, max_results: int) -> str:
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    response = requests.get(API_BASE, params=params)
    response.raise_for_status()
    return response.text
