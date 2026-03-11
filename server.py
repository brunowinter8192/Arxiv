# INFRASTRUCTURE
from typing import Annotated, Literal
from fastmcp import FastMCP
from pydantic import Field
from mcp.types import TextContent

from src.arxiv.search import search_workflow
from src.arxiv.get_paper import get_paper_workflow
from src.arxiv.download_paper import download_paper_workflow

mcp = FastMCP("ArXiv")


# TOOLS

@mcp.tool
def arxiv_search(
    query: Annotated[str, Field(description="Search query using ArXiv syntax. Prefix fields with ti: (title), au: (author), abs: (abstract), cat: (category), all: (all fields). Combine with AND, OR, ANDNOT. Example: 'ti:transformer AND cat:cs.CL'")],
    sort_by: Annotated[
        Literal["relevance", "lastUpdatedDate", "submittedDate"],
        Field(description="Sort by: relevance (default), lastUpdatedDate, or submittedDate")
    ] = "relevance",
    sort_order: Annotated[
        Literal["descending", "ascending"],
        Field(description="Sort order: descending (default) or ascending")
    ] = "descending",
    start: Annotated[int, Field(description="0-based index of first result (for paging)")] = 0,
    max_results: Annotated[int, Field(description="Max results to return (1-2000)")] = 10,
) -> list[TextContent]:
    """Search ArXiv papers by query. Use field prefixes (ti:, au:, abs:, cat:, all:) and Boolean operators (AND, OR, ANDNOT) to construct queries. Use submittedDate filter for date ranges: 'au:smith AND submittedDate:[202301010000 TO 202401010000]'."""
    return search_workflow(query, sort_by, sort_order, start, max_results)


@mcp.tool
def arxiv_get_paper(
    ids: Annotated[str, Field(description="Comma-separated ArXiv IDs (e.g., '2301.07041' or '2301.07041,2305.14314' or 'cond-mat/0207270')")],
) -> list[TextContent]:
    """Get full metadata for one or more ArXiv papers by their IDs. Returns title, authors, abstract, categories, dates, PDF link, DOI, and journal reference."""
    return get_paper_workflow(ids)


@mcp.tool
def arxiv_download_paper(
    arxiv_id: Annotated[str, Field(description="ArXiv paper ID (e.g., '2301.07041' or 'cond-mat/0207270v1')")],
    output_dir: Annotated[str, Field(description="Directory to save the PDF file")] = "/tmp/arxiv",
) -> list[TextContent]:
    """Download a paper's PDF from ArXiv. Saves to output_dir with filename based on ArXiv ID."""
    return download_paper_workflow(arxiv_id, output_dir)


if __name__ == "__main__":
    mcp.run()
