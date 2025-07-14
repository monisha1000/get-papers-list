import requests
import xml.etree.ElementTree as ET
from typing import List
from papers.models import Paper

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_pubmed_data(query: str, debug: bool = False) -> List[Paper]:
    ids = search_pubmed(query)
    if debug:
        print(f"Fetched PubMed IDs: {ids}")

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID", default="")
        title = article.findtext(".//ArticleTitle", default="No title")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        
        authors = article.findall(".//Author")
        non_academic_authors = []
        affiliations = []
        email = None

        for author in authors:
            aff = author.findtext(".//AffiliationInfo/Affiliation")
            if aff:
                affiliations.append(aff)
                if "@" in aff and not email:
                    email = aff.split()[-1]  # crude email grab
                if any(keyword in aff.lower() for keyword in ["inc", "ltd", "corp", "gmbh", "pharma", "biotech", "therapeutics"]):
                    name = author.findtext("ForeName", "") + " " + author.findtext("LastName", "")
                    non_academic_authors.append(name.strip())

        papers.append(Paper(
            pubmed_id=pmid,
            title=title,
            publication_date=pub_date,
            non_academic_authors=non_academic_authors,
            company_affiliations=affiliations,
            corresponding_author_email=email
        ))

    return papers
