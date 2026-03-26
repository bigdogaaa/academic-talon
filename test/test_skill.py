#!/usr/bin/env python3
"""Test script for the Paper Reader skill"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill import skill

def test_skill():
    """Test the Paper Reader skill"""
    print("Testing Paper Reader skill...")
    
    # Test case 1: Search with default engine weights
    print("\n=== Test 1: Search with default engine weights ===")
    input_data = {
        "action": "search",
        "query": "hallucination",
        "limit": 10,
        "source": "all"
    }
    result = skill.run(input_data)
    print(f"Success: {result.get('success')}")
    print(f"Total results: {len(result.get('results', []))}")
    
    # Test case 2: Search with custom engine weights
    print("\n=== Test 2: Search with custom engine weights ===")
    input_data_custom = {
        "action": "search",
        "query": "hallucination",
        "limit": 10,
        "source": "all",
        "engine_weights": {
            "arxiv": 3,
            "google_scholar": 4,
            "semantic_scholar": 2,
            "tavily": 1
        }
    }
    result_custom = skill.run(input_data_custom)
    print(f"Success: {result_custom.get('success')}")
    print(f"Total results: {len(result_custom.get('results', []))}")

if __name__ == "__main__":
    test_skill()
