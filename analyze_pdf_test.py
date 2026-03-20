from scripts.pdf_analyzer import analyze_pdf_header, analyze_pdf_fulltext, check_grobid_status
import traceback
import os

# Path to the PDF file
pdf_path = "./2405.10825v2.pdf"

# Check if PDF file exists
print(f"Checking if PDF file exists: {pdf_path}")
if not os.path.exists(pdf_path):
    print(f"PDF file not found: {pdf_path}")
else:
    print(f"PDF file found: {pdf_path}")

# Check if Grobid is running
print("\nChecking if Grobid is running...")
grobid_status = check_grobid_status()
print(f"Grobid status: {'Running' if grobid_status else 'Not running'}")

# Analyze the PDF header
try:
    print("\nAnalyzing PDF header...")
    header_xml = analyze_pdf_header(pdf_path)
    
    if header_xml:
        print("\n=== PDF Header Analysis Results ===")
        print(f"XML response length: {len(header_xml)}")
        print(f"XML response (first 500 chars): {header_xml[:500]}...")
        print("\n=== Header Analysis Complete ===")
    else:
        print("\n=== Header Analysis Failed ===")
except Exception as e:
    print(f"Error analyzing PDF header: {e}")
    print(traceback.format_exc())
    print("\n=== Header Analysis Failed ===")

# Analyze the PDF fulltext
try:
    print("\nAnalyzing PDF fulltext...")
    fulltext_xml = analyze_pdf_fulltext(pdf_path)
    
    if fulltext_xml:
        print("\n=== PDF Fulltext Analysis Results ===")
        print(f"XML response length: {len(fulltext_xml)}")
        print(f"XML response (first 500 chars): {fulltext_xml[:500]}...")
        print("\n=== Fulltext Analysis Complete ===")
    else:
        print("\n=== Fulltext Analysis Failed ===")
except Exception as e:
    print(f"Error analyzing PDF fulltext: {e}")
    print(traceback.format_exc())
    print("\n=== Fulltext Analysis Failed ===")