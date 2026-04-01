---
name: academic-talon
description: Use this skill when the user wants to search for academic papers, analyze PDF files, extract metadata, or save papers to Zotero.
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["python"],
      "env": [],
      "config": []
    },
    "install": [
      {
        "id": "pip-install-deps",
        "kind": "pip",
        "package": "-r requirements.txt",
        "label": "Install Python dependencies (requires Python 3)"
      }
    ],
    "emoji": "🎓",
    "notes": "This skill requires Zotero API credentials for archiving functionality and optional API keys for additional search engines. It uses GROBID for PDF parsing, which can be run locally or remotely."
  }
}
---

# Instructions

You are an academic research assistant.

Use this skill to:

- Search for academic papers
- Download and analyze PDF files
- Extract structured metadata (BibTeX or full text)
- Archive papers into Zotero

## When to use

Trigger this skill if the user:

- asks to find or search academic papers
- provides a PDF and wants analysis or metadata extraction
- wants to save or organize papers in Zotero
- asks for BibTeX or citation generation

## Actions

You MUST choose the correct action:

- `search` → find papers
- `download` → download PDF
- `analyze` → extract metadata or full text
- `archive` → save to Zotero

## Rules

- Always select the correct action based on user intent
- Prefer `search` before `download` if no URL is provided
- Use `analyze` to extract BibTeX before archiving
- Avoid duplicate archiving
- Return structured JSON results only

# Overview (Human Readable Documentation)

This skill provides a comprehensive solution for academic paper research and management. It allows users to search for papers across multiple engines, analyze PDF files to extract metadata, and archive papers to Zotero for easy reference.

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
3. **Optional Zotero archiving**
   - Archives papers to Zotero library (requires Zotero API credentials)
   - Adds PDF URL as link
   - Avoids duplicate entries
   - Adds items to specified collection (default: "openclaw")

## Quick Reference

| Situation               | Action                                                            |
| ----------------------- | ----------------------------------------------------------------- |
| Search for papers       | Use `search` action with query parameter                          |
| Analyze PDF header      | Use `analyze` action with pdf\_path and analysis\_type="header"   |
| Analyze PDF full text   | Use `analyze` action with pdf\_path and analysis\_type="fulltext" |
| Archive paper to Zotero | Use `archive` action with paper\_info parameter                   |

## OpenClaw Setup

### Installation

Via ClawdHub (recommended):

```bash
clawdhub install academic-talon
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the skill directory with the following variables:

```
# Zotero API credentials (optional, required only for archive functionality)
# ZOTERO_API_KEY=your_zotero_api_key
# ZOTERO_LIBRARY_ID=your_zotero_library_id
# ZOTERO_LIBRARY_TYPE=user # or group

# Optional API keys for additional search engines
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key # Optional
SERPAPI_KEY=your_serpapi_key # For Google Scholar
TAVILY_API_KEY=your_tavily_api_key # For Tavily

# GROBID API URL (default: http://localhost:8070/api)
GROBID_API_URL=http://localhost:8070/api
```

### Required Services

- **GROBID server** - You can start the server using one of the following methods:

  **Official Quick Start:**
  - Follow the instructions on the [GROBID Docker Hub page](https://hub.docker.com/r/grobid/grobid) or [Quick Start](https://grobid.readthedocs.io/en/latest/getting_started/).
  **Docker Compose Deployment:**
  - Create a `compose.yml` file with the following content:
  ```yaml
  version: "3.9"

  services:
    grobid:
      image: grobid/grobid:0.8.2-crf
      container_name: grobid
      restart: unless-stopped

      # ❗ Do not expose port externally
      expose:
        - "8070"

      environment:
        JAVA_OPTS: "-Xms512m -Xmx4g"
        GROBID_MAX_CONCURRENCY: "1"

      volumes:
        - ./grobid/tmp:/opt/grobid/tmp
        - ./grobid/logs:/opt/grobid/logs

      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:8070/api/isalive"]
        interval: 30s
        timeout: 5s
        retries: 5

      networks:
        - grobid-net

    nginx:
      image: nginx:latest
      container_name: grobid-nginx
      restart: unless-stopped

      ports:
        - "8080:8080"

      volumes:
        - ./nginx.conf:/etc/nginx/conf.d/default.conf
        # Uncomment the line below if you want to add username/password
        # - ./.htpasswd:/etc/nginx/.htpasswd

      depends_on:
        - grobid

      networks:
        - grobid-net

  networks:
    grobid-net:
  ```
  - Create an `nginx.conf` file with the following content:
  ```nginx
  server {
      listen 8080;

      location / {
          proxy_pass http://grobid:8070;

          # =========================
          # ✅ IP Whitelist (Important)
          # =========================
          allow 127.0.0.1;        # Localhost
          # allow 10.0.0.0/8;     # Internal network (optional)

          deny all;

          # =========================
          # 🔐 Optional: Basic Auth
          # =========================
          # auth_basic "Restricted";
          # auth_basic_user_file /etc/nginx/.htpasswd;

          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
      }
  }
  ```
  - Run `docker-compose up -d` to start the services
  **Default Configuration:**
  - GROBID API URL: `http://localhost:8070/api`
  - If using the provided Docker Compose setup, access GROBID at: `http://localhost:8080/api`

## Usage

### Search Papers

```python
from skill import skill

# Search for papers on "hallucination"
result = skill.run({
    "action": "search",
    "query": "hallucination",
    "limit": 5,
    "source": "all"
})

print(result)

# Search papers with custom engine weights
    result = skill.run({
        "action": "search",
        "query": "hallucination in AI",
        "limit": 10,
        "source": "all",
        "engine_weights": {
            "arxiv": 5,
            "google_scholar": 3,
            "semantic_scholar": 1,
            "tavily": 1
        }
    })

print(result)
```

### Download PDF

```python
from skill import skill

# Download PDF from URL with custom filename
result = skill.run({
    "action": "download",
    "url": "https://example.com/paper.pdf",
    "filename": "example_paper.pdf"
})

print(result)

# Download PDF with custom save directory
result = skill.run({
    "action": "download",
    "url": "https://example.com/paper.pdf",
    "save_dir": "/path/to/pdf/library"
})

print(result)

# Download PDF with paper info for citation key generation
result = skill.run({
    "action": "download",
    "url": "https://example.com/paper.pdf",
    "paper_info": {
        "title": "Paper Title",
        "authors": ["John Doe", "Jane Smith"],
        "year": "2024"
    }
})

print(result)
```

### Analyze PDF

```python
from skill import skill

# Analyze PDF header from local path
result = skill.run({
    "action": "analyze",
    "pdf_input": "/path/to/paper.pdf",
    "analysis_type": "header"
})

print(result)

# Analyze PDF full text from URL
result = skill.run({
    "action": "analyze",
    "pdf_input": "https://example.com/paper.pdf",
    "analysis_type": "fulltext"
})

print(result)
```

### Archive to Zotero

```python
from skill import skill

# Archive paper to Zotero
result = skill.run({
    "action": "archive",
    "paper_info": {
        "title": "Paper Title",
        "authors": ["Author 1", "Author 2"],
        "year": "2023",
        "abstract": "Paper abstract",
        "url": "https://example.com/paper",
        "pdf_url": "https://example.com/paper.pdf",
        "bibtex": "@article{...}"
    }
})

print(result)
```

## Input Schema

| Parameter       | Type    | Description                                                                      | Required       | Default                                                                 |
| --------------- | ------- | -------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------- |
| action          | string  | Action to perform ("search", "download", "analyze", "archive")                   | Yes            | "search"                                                                |
| query           | string  | Search query (for search action)                                                 | Yes (search)   | ""                                                                      |
| limit           | integer | Number of results to return (for search action)                                  | No             | 10                                                                      |
| source          | string  | Search source ("all", "semantic\_scholar", "arxiv", "google\_scholar", "tavily") | No             | "all"                                                                   |
| engine\_weights | object  | Dictionary of engine weights (for search action)                                 | No             | {"arxiv": 5, "google\_scholar": 3, "semantic\_scholar": 1, "tavily": 1} |
| url             | string  | URL of the PDF file (for download action)                                        | Yes (download) | ""                                                                      |
| filename        | string  | Filename to save the PDF as (for download action)                                | No             | None                                                                    |
| save\_dir       | string  | Directory to save the PDF in (for download action)                               | No             | None                                                                    |
| paper\_info     | object  | Paper information (for download and archive actions)                             | No             | {}                                                                      |
| collection      | string  | Name of the collection to add the paper to (for archive action)                  | No             | "openclaw"                                                              |
| pdf\_input      | string  | Path to local PDF file or URL to PDF (for analyze action)                        | Yes (analyze)  | ""                                                                      |
| analysis\_type  | string  | Type of analysis ("header", "fulltext")                                          | No             | "header"                                                                |

## Output Schema

### Search Action

```json
{
  "success": true,
  "action": "search",
  "query": "hallucination",
  "results": [
    {
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "year": "2023",
      "abstract": "Paper abstract",
      "url": "https://example.com/paper",
      "pdf_url": "https://example.com/paper.pdf",
      "source": "semantic_scholar"
    }
  ]
}
```

### Download Action

```json
{
  "success": true,
  "action": "download",
  "url": "https://example.com/paper.pdf",
  "pdf_path": "/path/to/downloaded/paper.pdf"
}
```

### Analyze Action

```json
{
  "success": true,
  "action": "analyze",
  "pdf_input": "/path/to/paper.pdf",
  "analysis_type": "header",
  "result": "@article{...}"
}
```

### Archive Action

```json
{
  "success": true,
  "action": "archive",
  "result": {
    "success": true,
    "item_id": "ABC123",
    "added_to_collection": true
  }
}
```

## Error Handling

The skill returns error messages in the following format:

```json
{
  "success": false,
  "error": "Error message"
}
```

Common errors include:

- Missing required parameters
- API key not configured
- GROBID server not accessible
- Zotero API errors

## Dependencies

- **Python 3.6+**
- **Required packages**:
  - requests
  - python-dotenv
  - pyzotero
  - flask

## Examples

### Example 1: Search for papers

```python
from skill import skill

# Search for papers on "artificial intelligence"
result = skill.run({
    "action": "search",
    "query": "artificial intelligence",
    "limit": 3,
    "source": "arxiv"
})

# Print results
if result["success"]:
    for i, paper in enumerate(result["results"]):
        print(f"{i+1}. {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Year: {paper['year']}")
        print(f"URL: {paper['url']}")
        print(f"PDF URL: {paper['pdf_url']}")
        print()
else:
    print(f"Error: {result['error']}")
```

### Example 2: Analyze PDF and archive to Zotero

```python
from skill import skill
import os

# Path to PDF file
pdf_path = os.path.join(os.path.dirname(__file__), "papers", "example.pdf")

# Analyze PDF header
analyze_result = skill.run({
    "action": "analyze",
    "pdf_input": pdf_path,
    "analysis_type": "header"
})

if analyze_result["success"]:
    # Archive to Zotero
    paper_info = {
        "title": "Example Paper",
        "authors": ["John Doe", "Jane Smith"],
        "year": "2023",
        "abstract": "This is an example paper",
        "url": "https://example.com/paper",
        "pdf_url": "https://example.com/paper.pdf",
        "bibtex": analyze_result["result"]
    }
    
    archive_result = skill.run({
        "action": "archive",
        "paper_info": paper_info
    })
    
    if archive_result["success"]:
        print("Paper archived successfully!")
        print(f"Item ID: {archive_result['result']['item_id']}")
    else:
        print(f"Error archiving paper: {archive_result['error']}")
else:
    print(f"Error analyzing PDF: {analyze_result['error']}")
```

## Troubleshooting

### Common Issues

1. **GROBID server not accessible**
   - Make sure GROBID server is running
   - Check the GROBID_API_URL in .env file
2. **Zotero API errors**
   - Verify ZOTERO_API_KEY and ZOTERO_LIBRARY_ID in .env file
   - Check Zotero API rate limits
3. **Search engines returning empty results**
   - For Google Scholar: Ensure SERPAPI_KEY is configured
   - For Tavily: Ensure TAVILY_API_KEY is configured
   - For Semantic Scholar: Consider adding SEMANTIC_SCHOLAR_API_KEY for higher rate limits
4. **PDF analysis failing**
   - Ensure PDF file is accessible
   - Check GROBID server status

### Logs

The skill logs errors to the console. For detailed debugging, check the console output.

## Security Considerations

### Data Privacy
- **PDF Processing**: When analyzing PDF files, the skill sends PDF content to the configured GROBID API endpoint. For maximum privacy, run GROBID locally using the provided Docker Compose setup.
- **API Keys**: Store API keys in the .env file and never commit them to version control.
- **File Storage**: Downloaded PDF files are stored in the `pdfs` directory within the skill's installation directory.

### Best Practices
- **Local GROBID**: Use the provided Docker Compose setup to run GROBID locally, ensuring PDF content is not sent to external services.
- **Restricted Zotero Access**: Create a dedicated Zotero API key with limited permissions for archiving.
- **Environment Variables**: Use environment variables for API keys instead of hardcoding them.
- **Network Security**: When using the Docker Compose setup, the GROBID service is not exposed externally, and the nginx proxy includes IP whitelist protection.

### Risk Mitigation
- The skill only processes PDF files from user-provided URLs or local files within the skill's `pdfs` directory.
- All file operations are restricted to the skill's installation directory, preventing unauthorized file access.
- The skill does not request elevated permissions or modify system files.
- The Docker Compose setup includes health checks and security best practices.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to [paper reader github](https://github.com/bigdogaaa/academic-talon).

## License

This project is licensed under the MIT License.
