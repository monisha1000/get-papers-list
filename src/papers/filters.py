from typing import List
from papers.models import Paper

# Heuristics to detect non-academic affiliations
EXCLUDE_KEYWORDS = [
    "university", "college", "institute", "school", "department", "hospital", "clinic", "faculty", "center", "centre", "unit"
]

def is_non_academic_affiliation(affiliation: str) -> bool:
    affiliation = affiliation.lower()
    return not any(keyword in affiliation for keyword in EXCLUDE_KEYWORDS)

def filter_non_academic_authors(papers: List[Paper], debug: bool = False) -> List[Paper]:
    filtered = []

    for paper in papers:
        if any(is_non_academic_affiliation(aff) for aff in paper.company_affiliations):
            filtered.append(paper)
            if debug:
                print(f"✔ Included: {paper.title}")
        elif debug:
            print(f"✖ Skipped (all affiliations academic): {paper.title}")

    return filtered
