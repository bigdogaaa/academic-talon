from scripts.pdf_analyzer import analyze_pdf_header, analyze_pdf_fulltext
import os

# Test PDF analysis functionality
print("=== Testing PDF Analysis ===")

# Path to the downloaded PDF
pdf_path = os.path.join(os.path.dirname(__file__), "pdfs", "test_hallucination_paper.pdf")

if not os.path.exists(pdf_path):
    print(f"PDF file not found: {pdf_path}")
    exit(1)

# Test header analysis
print("\n1. Testing Header Analysis:")
header_xml = analyze_pdf_header(pdf_path)
if header_xml:
    print("Header analysis successful")
    # Print first 500 characters of XML response
    print(f"Header XML (first 500 chars): {header_xml[:500]}...")
else:
    print("Header analysis failed")

# Test full text analysis
print("\n2. Testing Full Text Analysis:")
fulltext_xml = analyze_pdf_fulltext(pdf_path)
if fulltext_xml:
    print("Full text analysis successful")
    # Print first 500 characters of XML response
    print(f"Full text XML (first 500 chars): {fulltext_xml[:500]}...")
else:
    print("Full text analysis failed")

print("\n=== PDF Analysis Test Complete ===")
