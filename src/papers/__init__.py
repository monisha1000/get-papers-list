import typer
from papers.client import fetch_pubmed_data
from papers.exporter import export_to_csv
from papers.filters import filter_non_academic_authors

app = typer.Typer()

@app.command()
def get(query: str, file: str = "", debug: bool = False):
    """
    Fetch papers from PubMed, filter by pharma/biotech affiliations, and export results.
    """
    if debug:
        typer.echo(f"Searching PubMed for query: '{query}'")

    papers = fetch_pubmed_data(query, debug=debug)
    filtered = filter_non_academic_authors(papers, debug=debug)

    if file:
        export_to_csv(filtered, file)
        typer.echo(f"✅ Results saved to {file}")
    else:
        for paper in filtered:
            typer.echo(paper)

if __name__ == "__main__":
    app()
