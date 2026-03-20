from scripts.search import search_papers, download_pdf
from scripts.pdf_analyzer import analyze_pdf_header
from scripts.zotero_archiver import archive_paper
import os

# Test full workflow: search -> download -> analyze -> archive
print("=== Testing Full Workflow ===")

# Step 1: Search for hallucination-related papers
print("\nStep 1: Searching for hallucination-related papers...")
arxiv_papers = search_papers('hallucination', limit=1, source="arxiv")

if not arxiv_papers:
    print("No papers found")
    exit(1)

paper = arxiv_papers[0]
print(f"Found paper: {paper.get('title')}")
print(f"Authors: {', '.join(paper.get('authors', []))}")
print(f"Year: {paper.get('year')}")
print(f"URL: {paper.get('url')}")
print(f"PDF URL: {paper.get('pdf_url')}")

# Step 2: Download PDF
print("\nStep 2: Downloading PDF...")
if paper.get('pdf_url'):
    pdf_url = paper.get('pdf_url')
    filename = f"{paper.get('title', 'unknown').replace(' ', '_').replace('/', '_').replace('\\', '_')}_{paper.get('year', 'unknown')}.pdf"
    print(f"Downloading PDF from: {pdf_url}")
    pdf_path = download_pdf(pdf_url, filename)
    if not pdf_path:
        print("Failed to download PDF")
        exit(1)
    print(f"PDF downloaded successfully: {pdf_path}")
else:
    print("No PDF URL available")
    exit(1)

# Step 3: Analyze PDF header to get BibTeX
print("\nStep 3: Analyzing PDF header...")
bibtex = analyze_pdf_header(pdf_path)
if not bibtex:
    print("Failed to analyze PDF header")
    exit(1)
print("PDF header analysis successful")

# Step 4: Archive to Zotero
print("\nStep 4: Archiving to Zotero...")
paper_info = {
    "title": paper.get('title'),
    "authors": paper.get('authors', []),
    "year": paper.get('year'),
    "abstract": paper.get('abstract'),
    "url": paper.get('url'),
    "pdf_url": paper.get('pdf_url'),
    "bibtex": bibtex
}

try:
    result = archive_paper(paper_info, use_pyzotero=True)
    print(f"Archiving result: {result}")
    
    if result.get("success"):
        print("✓ Zotero archiving successful!")
        print(f"Item ID: {result['item_id']}")
        
        if result.get("added_to_collection"):
            print("✓ Item added to openclaw collection")
        else:
            print("⚠ Item not added to openclaw collection")
    else:
        print("✗ Zotero archiving failed")
        print(f"Error: {result.get('error', 'Unknown error')}")
except Exception as e:
    print(f"Error during Zotero archiving: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Full Workflow Test Complete ===")
