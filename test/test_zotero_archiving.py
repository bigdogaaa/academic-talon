import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.zotero_archiver import archive_paper
from scripts.pdf_analyzer import analyze_pdf_header

# Test Zotero archiving functionality
print("=== Testing Zotero Archiving ===")

# Path to the downloaded PDF
pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pdfs", "test_hallucination_paper.pdf")

if not os.path.exists(pdf_path):
    print(f"PDF file not found: {pdf_path}")
    exit(1)

# Get BibTeX information from PDF header analysis
bibtex = analyze_pdf_header(pdf_path)

# Prepare paper information
paper_info = {
    "title": "MedForge: Interpretable Medical Deepfake Detection via Forgery-aware Reasoning",
    "authors": ["Zhihui Chen", "Kai He", "Qingyuan Lei", "Bin Pu", "Jian Zhang", "Yuling Xu", "Mengling Feng"],
    "year": "2026",
    "abstract": "Text-guided image editors can now manipulate authentic medical scans with high fidelity, enabling lesion implantation/removal that threatens clinical trust and safety. Existing defenses are inadequate for healthcare. Medical detectors are largely black-box, while M...",
    "url": "https://arxiv.org/abs/2603.18577v1",
    "pdf_url": "https://arxiv.org/pdf/2603.18577v1",
    "bibtex": bibtex
}

# Test Zotero archiving
print("\nArchiving paper to Zotero...")
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

print("\n=== Zotero Archiving Test Complete ===")
