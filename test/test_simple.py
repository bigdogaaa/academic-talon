from scripts.search import search_papers

# Test basic search with BibTeX generation
print("Testing basic search with BibTeX generation...")
papers = search_papers('hallucination', limit=2, source='arxiv')
print(f"Found {len(papers)} papers")

for i, p in enumerate(papers):
    print(f"\nPaper {i+1}: {p['title'][:50]}...")
    print(f"  Authors: {', '.join(p['authors'][:2])}...")
    print(f"  Year: {p['year']}")
    print(f"  Has BibTeX: {'Yes' if p['bibtex'] else 'No'}")
    if p['bibtex']:
        print(f"  BibTeX preview: {p['bibtex'][:100]}...")

print("\nTest completed successfully!")