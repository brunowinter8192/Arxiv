# INFRASTRUCTURE
import requests
from mcp.types import TextContent

from src.arxiv.parsing import API_BASE, parse_feed
from src.arxiv.formatting import format_paper_detail


# ORCHESTRATOR
def get_paper_workflow(ids: str) -> list[TextContent]:
    raw_xml = fetch_by_ids(ids)
    data = parse_feed(raw_xml)
    formatted = format_paper_detail(data)
    return [TextContent(type="text", text=formatted)]


# FUNCTIONS

def fetch_by_ids(ids: str) -> str:
    params = {"id_list": ids}
    response = requests.get(API_BASE, params=params)
    response.raise_for_status()
    return response.text
