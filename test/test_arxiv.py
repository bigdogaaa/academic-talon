from scripts.search import search_arxiv

# Test arXiv search
print('=== arXiv Results ===')
papers = search_arxiv('hallucination', limit=5)
for i, p in enumerate(papers):
    print(f'[{i+1}] {p['title']}')
    print(f'  Authors: {', '.join(p['authors'][:3])}{' et al.' if len(p['authors'])>3 else ''}')
    print(f'  Year: {p['year']}')
    print(f'  URL: {p['url']}')
    print(f'  Categories: {', '.join(p['categories'])}')
    print()
