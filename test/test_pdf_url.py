#!/usr/bin/env python3
"""Test script for PDF URL analysis and archiving"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill import skill

def test_pdf_url():
    """Test PDF URL analysis and archiving"""
    print("Testing PDF URL analysis and archiving...")
    
    # Test PDF URL (example from arXiv)
    pdf_url = "https://arxiv.org/pdf/2202.03629.pdf"
    
    # Test case 1: Analyze PDF header from URL
    print("\n=== Test 1: Analyze PDF header from URL ===")
    analyze_input = {
        "action": "analyze",
        "pdf_input": pdf_url,
        "analysis_type": "header"
    }
    analyze_result = skill.run(analyze_input)
    print(f"Success: {analyze_result.get('success')}")
    if analyze_result.get('success'):
        print(f"Analysis result (first 500 chars): {analyze_result.get('result', '')[:500]}...")
    
    # Test case 2: Download PDF
    print("\n=== Test 2: Download PDF ===")
    download_input = {
        "action": "download",
        "url": pdf_url
    }
    download_result = skill.run(download_input)
    print(f"Success: {download_result.get('success')}")
    if download_result.get('success'):
        print(f"PDF downloaded to: {download_result.get('pdf_path')}")

if __name__ == "__main__":
    test_pdf_url()
