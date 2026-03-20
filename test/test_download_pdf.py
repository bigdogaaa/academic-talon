from scripts.search import download_pdf
pdf_path = download_pdf("https://arxiv.org/pdf/2305.13245.pdf", "2305.13245.pdf")
print(f"Downloaded PDF: {pdf_path}")