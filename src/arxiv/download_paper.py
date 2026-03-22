# INFRASTRUCTURE
import logging
import os
import requests
from mcp.types import TextContent

from src.arxiv.parsing import API_BASE, parse_feed

logger = logging.getLogger(__name__)


# ORCHESTRATOR
def download_paper_workflow(arxiv_id: str, output_dir: str) -> list[TextContent]:
    logger.info("download_paper arxiv_id=%s output_dir=%s", arxiv_id, output_dir)
    raw_xml = fetch_by_id(arxiv_id)
    data = parse_feed(raw_xml)

    if not data["papers"]:
        return [TextContent(type="text", text=f"Paper {arxiv_id} not found.")]

    paper = data["papers"][0]
    pdf_url = paper["pdf_link"]
    if not pdf_url:
        return [TextContent(type="text", text=f"No PDF link for {arxiv_id}.")]

    os.makedirs(output_dir, exist_ok=True)
    safe_id = arxiv_id.replace("/", "_")
    filepath = os.path.join(output_dir, f"{safe_id}.pdf")

    download_pdf(pdf_url, filepath)

    result = f"Downloaded: {filepath}\nTitle: {paper['title']}\nAuthors: {', '.join(paper['authors'])}"
    return [TextContent(type="text", text=result)]


# FUNCTIONS

def fetch_by_id(arxiv_id: str) -> str:
    logger.debug("Fetching from %s", API_BASE)
    params = {"id_list": arxiv_id}
    response = requests.get(API_BASE, params=params)
    response.raise_for_status()
    return response.text


def download_pdf(url: str, filepath: str) -> None:
    logger.debug("Downloading PDF from %s", url)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
