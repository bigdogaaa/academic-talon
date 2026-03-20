import os
import json
from scripts.search import search_papers

# Test the enhanced search functionality
def test_search_functionality():
    print("=== Testing Enhanced Search Functionality ===")
    
    # Test 1: Basic search with BibTeX generation
    print("\n1. Testing basic search with BibTeX generation:")
    papers = search_papers('hallucination', limit=3, source="arxiv")
    for i, paper in enumerate(papers):
        print(f"\nPaper {i+1}:")
        print(json.dumps(paper, ensure_ascii=False, indent=2))
    
    # Test 2: Search with all sources
    print("\n\n2. Testing search with all sources:")
    papers = search_papers('hallucination', limit=5, source="all")
    print(f"Found {len(papers)} papers from all sources")
    for i, paper in enumerate(papers):
        print(f"\nPaper {i+1}:")
        print(json.dumps(paper, ensure_ascii=False, indent=2))
    
    # Test 3: Test PDF analysis (if PDF path is provided)
    print("\n\n3. Testing PDF analysis:")
    # Note: You can add a test PDF path here to test PDF analysis
    # test_pdf_path = "path/to/test/paper.pdf"
    # if os.path.exists(test_pdf_path):
    #     paper_with_pdf = {
    #         "title": "Test Paper",
    #         "authors": ["John Doe", "Jane Smith"],
    #         "year": "2023",
    #         "pdf_path": test_pdf_path
    #     }
    #     from scripts.pdf_analyzer import analyze_pdf
    #     pdf_info = analyze_pdf(test_pdf_path)
    #     print(f"PDF Analysis Results:")
    #     print(f"Title: {pdf_info.get('title')}")
    #     print(f"Authors: {', '.join(pdf_info.get('authors', []))}")
    #     print(f"Year: {pdf_info.get('year')}")
    #     print(f"Abstract: {pdf_info.get('abstract', '')[:100]}...")
    #     print(f"Has BibTeX: { 'Yes' if pdf_info.get('bibtex') else 'No' }")
    # else:
    print("No test PDF provided. Skipping PDF analysis test.")
    
    # Test 4: Test Zotero archiving (if API keys are provided)
    print("\n\n4. Testing Zotero archiving:")
    zotero_api_key = os.getenv("ZOTERO_API_KEY")
    zotero_library_id = os.getenv("ZOTERO_LIBRARY_ID")
    if zotero_api_key and zotero_library_id:
        print("Zotero API keys found. Testing Zotero archiving...")
        # Test with a single paper
        test_paper = papers[0] if papers else None
        if test_paper:
            from scripts.zotero_archiver import archive_paper
            result = archive_paper(test_paper)
            print(f"Zotero archiving result: {'Success' if 'success' in result else 'Failed'}")
            if 'error' in result:
                print(f"Error: {result['error']}")
    else:
        print("Zotero API keys not found. Skipping Zotero archiving test.")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_search_functionality()