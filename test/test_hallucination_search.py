from scripts.search import search_papers, download_pdf

# Test search for hallucination-related papers
print("=== Testing Hallucination Search ===")

# Test Semantic Scholar search
print("\n1. Semantic Scholar:")
semantic_scholar_papers = search_papers('hallucination', limit=1, source="semantic_scholar")
if semantic_scholar_papers:
    paper = semantic_scholar_papers[0]
    print(f"Title: {paper.get('title')}")
    print(f"Authors: {', '.join(paper.get('authors', []))}")
    print(f"Year: {paper.get('year')}")
    print(f"URL: {paper.get('url')}")
    print(f"PDF URL: {paper.get('pdf_url')}")
else:
    print("No results found")

# Test arXiv search
print("\n2. arXiv:")
arxiv_papers = search_papers('hallucination', limit=1, source="arxiv")
if arxiv_papers:
    paper = arxiv_papers[0]
    print(f"Title: {paper.get('title')}")
    print(f"Authors: {', '.join(paper.get('authors', []))}")
    print(f"Year: {paper.get('year')}")
    print(f"URL: {paper.get('url')}")
    print(f"PDF URL: {paper.get('pdf_url')}")
else:
    print("No results found")

# Test Google Scholar search
print("\n3. Google Scholar:")
google_scholar_papers = search_papers('hallucination', limit=1, source="google_scholar")
if google_scholar_papers:
    paper = google_scholar_papers[0]
    print(f"Title: {paper.get('title')}")
    print(f"Authors: {', '.join(paper.get('authors', []))}")
    print(f"Year: {paper.get('year')}")
    print(f"URL: {paper.get('url')}")
    print(f"PDF URL: {paper.get('pdf_url')}")
else:
    print("No results found")

# Test Tavily search
print("\n4. Tavily:")
tavily_papers = search_papers('hallucination', limit=1, source="tavily")
if tavily_papers:
    paper = tavily_papers[0]
    print(f"Title: {paper.get('title')}")
    print(f"Authors: {', '.join(paper.get('authors', []))}")
    print(f"Year: {paper.get('year')}")
    print(f"URL: {paper.get('url')}")
    print(f"PDF URL: {paper.get('pdf_url')}")
else:
    print("No results found")

# Download a PDF for testing
print("\n=== Downloading PDF for Testing ===")
if arxiv_papers and arxiv_papers[0].get('pdf_url'):
    pdf_url = arxiv_papers[0].get('pdf_url')
    filename = "test_hallucination_paper.pdf"
    print(f"Downloading PDF from: {pdf_url}")
    pdf_path = download_pdf(pdf_url, filename)
    if pdf_path:
        print(f"PDF downloaded successfully: {pdf_path}")
    else:
        print("Failed to download PDF")
else:
    print("No PDF URL available for download")

print("\n=== Search Test Complete ===")
