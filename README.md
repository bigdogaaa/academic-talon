# Paper Reader Skill

A skill for searching academic papers, analyzing PDFs, and archiving to Zotero.

## Features

1. **Multi-engine paper search**
   - Semantic Scholar
   - arXiv
   - Google Scholar (via SerpAPI)
   - Tavily

2. **PDF analysis**
   - Header analysis (returns BibTeX format)
   - Full text analysis (returns XML format)
   - Uses GROBID API for parsing

3. **Zotero archiving**
   - Archives papers to Zotero library
   - Adds PDF URL as link
   - Avoids duplicate entries
   - Adds items to "openclaw" collection

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/paper-reader.git
   cd paper-reader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   # Zotero API credentials
   ZOTERO_API_KEY=your_zotero_api_key
   ZOTERO_LIBRARY_ID=your_zotero_library_id
   ZOTERO_LIBRARY_TYPE=user # or group

   # Optional API keys for additional search engines
   SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key # Optional
   SERPAPI_KEY=your_serpapi_key # For Google Scholar
   TAVILY_API_KEY=your_tavily_api_key # For Tavily

   # GROBID API URL (default: http://localhost:8070/api)
   GROBID_API_URL=http://localhost:8070/api
   ```

4. **Start GROBID server**
   Follow the instructions on the [GROBID GitHub page](https://github.com/kermitt2/grobid) to start the server.

## Usage

### Search papers

```python
from scripts.search import search_papers

# Search for papers on "hallucination"
papers = search_papers("hallucination", limit=5)

# Print results
for i, paper in enumerate(papers):
    print(f"{i+1}. {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Year: {paper['year']}")
    print(f"URL: {paper['url']}")
    print(f"PDF URL: {paper['pdf_url']}")
    print()
```

### Analyze PDF

```python
from scripts.pdf_analyzer import analyze_pdf_header, analyze_pdf_fulltext

# Path to PDF file
pdf_path = "path/to/paper.pdf"

# Analyze header (returns BibTeX)
bibtex = analyze_pdf_header(pdf_path)
print("BibTeX:")
print(bibtex)

# Analyze full text (returns XML)
xml = analyze_pdf_fulltext(pdf_path)
print("\nFull text XML:")
print(xml)
```

### Archive to Zotero

```python
from scripts.zotero_archiver import archive_paper

# Paper information
paper_info = {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "year": "2023",
    "abstract": "Paper abstract",
    "url": "https://example.com/paper",
    "pdf_url": "https://example.com/paper.pdf",
    "bibtex": "@article{...}"
}

# Archive to Zotero
result = archive_paper(paper_info, use_pyzotero=True)
print(f"Archiving result: {result}")
```

## Testing

Run the test scripts to verify functionality:

```bash
# Test paper search
python test_hallucination_search.py

# Test PDF analysis
python test_pdf_analysis.py

# Test Zotero archiving
python test_zotero_archiving.py

# Test full workflow
python test_full_workflow.py
```

## Skill Integration

This project can be integrated as a skill in platforms like OpenClaw. The `package.json` file defines the skill configuration, including triggers and input schema.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
