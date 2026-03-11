# INFRASTRUCTURE
import os
import requests
from mcp.types import TextContent

from src.arxiv.parsing import API_BASE, parse_feed


# ORCHESTRATOR
def download_paper_workflow(arxiv_id: str, output_dir: str) -> list[TextContent]:
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
    filename = f"{safe_id}.pdf"
    filepath = os.path.join(output_dir, filename)

    download_pdf(pdf_url, filepath)

    result = f"Downloaded: {filepath}\nTitle: {paper['title']}\nAuthors: {', '.join(paper['authors'])}"
    return [TextContent(type="text", text=result)]


# FUNCTIONS

def fetch_by_id(arxiv_id: str) -> str:
    params = {"id_list": arxiv_id}
    response = requests.get(API_BASE, params=params)
    response.raise_for_status()
    return response.text


def download_pdf(url: str, filepath: str) -> None:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
