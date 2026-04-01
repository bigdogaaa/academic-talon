#!/usr/bin/env python3
"""
Test script for the full flow: PDF header analysis -> save to Zotero
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pdf_analyzer import analyze_pdf_header
from scripts.zotero_archiver import archive_paper

# Load environment variables
load_dotenv()

# Test PDF file path
# Use an existing PDF in the pdfs directory
test_pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdfs', 'Test_Paper_on_Hallucination_2023.pdf')

if not os.path.exists(test_pdf_path):
    print(f"Test PDF file not found: {test_pdf_path}")
    print("Please ensure you have a test PDF file in the pdfs directory")
    sys.exit(1)

print("=== Testing Full Flow: PDF Analysis -> Zotero Archive ===")
print(f"Test PDF: {test_pdf_path}")
print()

# Step 1: Analyze PDF header
print("Step 1: Analyzing PDF header...")
try:
    xml_response = analyze_pdf_header(test_pdf_path)
    if xml_response:
        print("✓ PDF header analysis successful")
        # Print first 500 characters of XML response for debugging
        print(f"XML response (first 500 chars): {xml_response[:500]}...")
    else:
        print("✗ PDF header analysis failed")
        sys.exit(1)
except Exception as e:
    print(f"Error analyzing PDF header: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Step 2: Prepare paper info
print("Step 2: Preparing paper information...")
paper_info = {
    "title": "Test Paper on Hallucination",
    "authors": ["John Doe", "Jane Smith"],
    "year": "2023",
    "abstract": "This is a test paper about hallucination in LLMs",
    "url": "https://example.com/test-paper",
    "pdf_path": test_pdf_path
}
print(f"Paper info: {paper_info}")

print()

# Step 3: Archive to Zotero
print("Step 3: Archiving to Zotero...")
try:
    # Add PDF URL to paper info for attachment
    paper_info["pdf_url"] = "https://example.com/test-paper.pdf"  # Example PDF URL
    
    # Use pyzotero for archiving
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

print()
print("=== Full Flow Test Complete ===")
