# INFRASTRUCTURE
from typing import Literal
from fastmcp import FastMCP
from mcp.types import TextContent

from src.arxiv.search import search_workflow
from src.arxiv.get_paper import get_paper_workflow
from src.arxiv.download_paper import download_paper_workflow

mcp = FastMCP("ArXiv")


# TOOLS

@mcp.tool
def arxiv_search(
    query: str,
    sort_by: Literal["relevance", "lastUpdatedDate", "submittedDate"] = "relevance",
    sort_order: Literal["descending", "ascending"] = "descending",
    start: int = 0,
    max_results: int = 10,
) -> list[TextContent]:
    """Search ArXiv papers."""
    return search_workflow(query, sort_by, sort_order, start, max_results)


@mcp.tool
def arxiv_get_paper(ids: str) -> list[TextContent]:
    """Get paper metadata by ArXiv ID."""
    return get_paper_workflow(ids)


@mcp.tool
def arxiv_download_paper(arxiv_id: str, output_dir: str) -> list[TextContent]:
    """Download paper PDF."""
    return download_paper_workflow(arxiv_id, output_dir)


if __name__ == "__main__":
    mcp.run()
