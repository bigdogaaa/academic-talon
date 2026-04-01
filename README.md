# Academic Talon Skill

## About

This is the base repository for the [Academic Talon skill](https://clawhub.ai/bigdogaaa/academic-talon), which provides functionality for searching academic papers, analyzing PDFs, and archiving to Zotero. This repository includes the core skill code as well as additional test scripts for verifying functionality.

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
   git clone https://github.com/bigdogaaa/academic-talon.git
   cd academic-talon
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
   You can start the server using one of the following methods:

   **Official Quick Start:**
   - Follow the instructions on the [GROBID Docker Hub page](https://hub.docker.com/r/grobid/grobid)

   **Docker Compose Deployment:**
   - Create a `compose.yml` file with the following content:
   
   ```yaml
   version: "3.9"

   services:
     grobid:
       image: docker.1ms.run/grobid/grobid:0.8.2-crf
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
       image: docker.1ms.run/nginx:latest
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

This repository includes additional test scripts in the `test` directory for verifying functionality:

```bash
# Test paper search with engine weight distribution
python test/test_search.py

# Test the complete skill functionality
python test/test_skill.py

# Test PDF URL analysis and download
python test/test_pdf_url.py
```

## Skill Integration

This project can be integrated as a skill in platforms like OpenClaw. The `package.json` file defines the skill configuration, including triggers and input schema.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
