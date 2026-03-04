# AI Engineering Course

[🇺🇸 Read in English](README.en.md) | [🇧🇷 Ler em português do Brasil](README.md)

Project developed as part of the AI Engineering specialization course. This repository contains practical examples and implementations of AI concepts, including document processing, RAG (Retrieval-Augmented Generation), and financial data ingestion.

## 📋 Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- API Keys:
  - Groq API Key
  - OpenAI API Key
  - Qdrant URL and API Key
  - Valid email for Edgar API

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd curso-ia
```

2. Install dependencies with `uv`:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp ../.env.example .env
```

Edit the `.env` file with your credentials:
```env
GROQ_API_KEY="your-groq-key"
OPENAI_API_KEY="your-openai-key"
QDRANT_URL="your-qdrant-url"
QDRANT_API_KEY="your-qdrant-key"
EDGAR_EMAIL="your-email"
```

## 📁 Project Structure

```
curso-ia/
├── docling/          # Document extraction and processing (PDFs)
├── projeto/          # Main project with financial data ingestion
├── Rag/              # RAG (Retrieval-Augmented Generation) implementations
├── db/               # Local database
├── images/           # Image assets
└── main.py           # Main entry point
```

## 📚 Modules

### 1. Docling (Document Processing)

Module focused on extracting content from PDF documents using the [Docling](https://github.com/DS4SD/docling) library.

**Available scripts:**

| File | Description |
|------|-------------|
| `1-extraction.py` | Basic text extraction from PDFs (local or URL) |
| `2-extraction-images.py` | Text extraction with images |
| `3-chunking.py` | Splitting documents into chunks |
| `4-hybrid-chunker.py` | Hybrid document chunking |
| `5-metadados.py` | Metadata extraction and manipulation |
| `6-embeddings.py` | Generating embeddings for documents |

**Usage example:**
```bash
uv run docling/1-extraction.py
```

### 2. RAG (Retrieval-Augmented Generation)

RAG system implementations for retrieving and generating responses based on documents.

**Scripts:**
- `rag.py` - Basic RAG implementation with Groq and SentenceTransformers
- `rag-qdrant.py` - RAG using Qdrant as vector database

### 3. Main Project

Complete system for ingestion and processing of financial data (SEC 10-K and 10-Q forms).

**Files:**
- `ingestion.py` - Financial data ingestion from Edgar API
- `create_collection.py` - Qdrant collection creation
- `test-query.py` - Script for testing queries
- `utils/` - Utilities (semantic chunker, Edgar client)
- `app/` - Main application

**Technologies used:**
- **FastEmbed** - Dense, sparse, and ColBERT embeddings
- **Qdrant** - Vector database
- **FastAPI** - REST API
- **Groq** - LLM for response generation
- **HDBSCAN** - Clustering

## 🔧 Useful Commands

```bash
# Run main script
uv run main.py

# Run Docling scripts
uv run docling/1-extraction.py

# Run data ingestion
uv run projeto/ingestion.py

# Run RAG
uv run Rag/rag.py

# Start API server (if available)
uv run uvicorn projeto.app.main:app --reload
```

## 📝 Docling Scripts Description

1. **Extraction (`1-extraction.py`)**: Converts PDFs to structured Markdown
2. **Extraction with Images (`2-extraction-images.py`)**: Extracts text and images from documents
3. **Chunking (`3-chunking.py`)**: Splits documents into smaller parts for processing
4. **Hybrid Chunker (`4-hybrid-chunker.py`)**: Advanced document splitting strategies
5. **Metadata (`5-metadados.py`)**: Extracts and organizes document metadata
6. **Embeddings (`6-embeddings.py`)**: Generates vector representations of documents

## 🛠️ Main Dependencies

- `docling` - Document processing
- `qdrant-client` - Vector database
- `fastembed` - Embedding generation
- `groq` - LLM API
- `openai` - OpenAI API
- `sentence-transformers` - Embedding models
- `fastapi` + `uvicorn` - Web server
- `python-dotenv` - Environment variable management

## 📄 License

This project is licensed under the [MIT](../LICENSE) license.

## 🤝 Contributing

This is an academic project. Contributions, issues, and suggestions are welcome!
