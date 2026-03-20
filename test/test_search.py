#!/usr/bin/env python3
"""Test script for the search functionality with engine weight distribution"""

import os
import sys
import traceback

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.search import search_papers

def test_search():
    """Test the search functionality with engine weight distribution"""
    print("Testing search functionality with engine weight distribution...")
    
    try:
        # Test case 1: Default engine weights (arxiv:5, google_scholar:3, semantic_scholar:1, tavily:1)
        print("\n=== Test 1: Default engine weights ===")
        print("Searching for 'hallucination' with limit=10...")
        papers = search_papers('hallucination', limit=10, source="all")
        print(f"Total papers found: {len(papers)}")
        
        # Test case 2: Custom engine weights
        print("\n=== Test 2: Custom engine weights ===")
        custom_weights = {
            "arxiv": 3,
            "google_scholar": 4,
            "semantic_scholar": 2,
            "tavily": 1
        }
        print(f"Searching with custom weights: {custom_weights}")
        papers_custom = search_papers('hallucination', limit=10, source="all", engine_weights=custom_weights)
        print(f"Total papers found with custom weights: {len(papers_custom)}")
    except Exception as e:
        print(f"Error during test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_search()
