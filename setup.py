from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="paper-reader-skill",
    version="1.0.0",
    description="A skill for searching academic papers, analyzing PDFs, and archiving to Zotero",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/paper-reader",
    packages=find_packages(),
    package_data={
        "": ["*.md", "*.json"],
    },
    include_package_data=True,
    install_requires=[
        "requests",
        "python-dotenv",
        "pyzotero",
        "flask"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
