import pandas as pd
from typing import List
from papers.models import Paper

def export_to_csv(papers: List[Paper], filename: str) -> None:
    rows = []
    for paper in papers:
        rows.append({
            "PubmedID": paper.pubmed_id,
            "Title": paper.title,
            "Publication Date": paper.publication_date,
            "Non-academic Author(s)": "; ".join(paper.non_academic_authors),
            "Company Affiliation(s)": "; ".join(paper.company_affiliations),
            "Corresponding Author Email": paper.corresponding_author_email or ""
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
