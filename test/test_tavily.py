import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.search import search_tavily

# Test Tavily search
print('=== Tavily Results ===')
papers = search_tavily('hallucination', limit=5)
for i, p in enumerate(papers):
    print(f'[{i+1}] {p['title']}')
    print(f'  Authors: {', '.join(p['authors'][:3])}{' et al.' if len(p['authors'])>3 else ''}')
    print(f'  Year: {p['year']}')
    print(f'  URL: {p['url']}')
    print()
