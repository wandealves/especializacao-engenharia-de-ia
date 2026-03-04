# Curso de Engenharia de IA

[🇺🇸 Read in English](README.en.md) | [🇧🇷 Ler em português do Brasil](README.md)

Projeto desenvolvido como parte do curso de especialização em Engenharia de Inteligência Artificial. Este repositório contém exemplos práticos e implementações de conceitos de IA, incluindo processamento de documentos, RAG (Retrieval-Augmented Generation) e ingestão de dados financeiros.

## 📋 Pré-requisitos

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python)
- Chaves de API:
  - Groq API Key
  - OpenAI API Key
  - Qdrant URL e API Key
  - Email válido para API da Edgar

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd curso-ia
```

2. Instale as dependências com `uv`:
```bash
uv sync
```

3. Configure as variáveis de ambiente:
```bash
cp ../.env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
GROQ_API_KEY="sua-chave-groq"
OPENAI_API_KEY="sua-chave-openai"
QDRANT_URL="url-do-qdrant"
QDRANT_API_KEY="sua-chave-qdrant"
EDGAR_EMAIL="seu-email"
```

## 📁 Estrutura do Projeto

```
curso-ia/
├── docling/          # Extração e processamento de documentos (PDFs)
├── projeto/          # Projeto principal com ingestão de dados financeiros
├── Rag/              # Implementações de RAG (Retrieval-Augmented Generation)
├── db/               # Banco de dados local
├── images/           # Assets de imagens
└── main.py           # Ponto de entrada principal
```

## 📚 Módulos

### 1. Docling (Processamento de Documentos)

Módulo focado na extração de conteúdo de documentos PDF usando a biblioteca [Docling](https://github.com/DS4SD/docling).

**Scripts disponíveis:**

| Arquivo | Descrição |
|---------|-----------|
| `1-extraction.py` | Extração básica de texto de PDFs (local ou URL) |
| `2-extraction-images.py` | Extração de texto com imagens |
| `3-chunking.py` | Divisão de documentos em chunks |
| `4-hybrid-chunker.py` | Chunking híbrido de documentos |
| `5-metadados.py` | Extração e manipulação de metadados |
| `6-embeddings.py` | Geração de embeddings para documentos |

**Exemplo de uso:**
```bash
uv run docling/1-extraction.py
```

### 2. RAG (Retrieval-Augmented Generation)

Implementações de sistemas RAG para recuperação e geração de respostas baseadas em documentos.

**Scripts:**
- `rag.py` - Implementação básica de RAG com Groq e SentenceTransformers
- `rag-qdrant.py` - RAG utilizando Qdrant como vetor de banco de dados

### 3. Projeto Principal

Sistema completo de ingestão e processamento de dados financeiros (formulários SEC 10-K e 10-Q).

**Arquivos:**
- `ingestion.py` - Ingestão de dados financeiros da API Edgar
- `create_collection.py` - Criação de coleção no Qdrant
- `test-query.py` - Script para testar queries no sistema
- `utils/` - Utilitários (semantic chunker, Edgar client)
- `app/` - Aplicação principal

**Tecnologias utilizadas:**
- **FastEmbed** - Geração de embeddings densos, esparsos e ColBERT
- **Qdrant** - Banco de dados vetorial
- **FastAPI** - API REST
- **Groq** - LLM para geração de respostas
- **HDBSCAN** - Clustering

## 🔧 Comandos Úteis

```bash
# Rodar o script principal
uv run main.py

# Rodar scripts do Docling
uv run docling/1-extraction.py

# Rodar ingestão de dados
uv run projeto/ingestion.py

# Rodar RAG
uv run Rag/rag.py

# Iniciar servidor API (se disponível)
uv run uvicorn projeto.app.main:app --reload
```

## 📝 Descrição dos Scripts Docling

1. **Extração (`1-extraction.py`)**: Converte PDFs para Markdown estruturado
2. **Extração com Imagens (`2-extraction-images.py`)**: Extrai texto e imagens de documentos
3. **Chunking (`3-chunking.py`)**: Divide documentos em partes menores para processamento
4. **Hybrid Chunker (`4-hybrid-chunker.py`)**: Estratégias avançadas de divisão de documentos
5. **Metadados (`5-metadados.py`)**: Extrai e organiza metadados dos documentos
6. **Embeddings (`6-embeddings.py`)**: Gera representações vetoriais dos documentos

## 🛠️ Dependências Principais

- `docling` - Processamento de documentos
- `qdrant-client` - Banco de dados vetorial
- `fastembed` - Geração de embeddings
- `groq` - API para LLMs
- `openai` - API OpenAI
- `sentence-transformers` - Modelos de embedding
- `fastapi` + `uvicorn` - Servidor web
- `python-dotenv` - Gerenciamento de variáveis de ambiente

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](../LICENSE).

## 🤝 Contribuição

Este é um projeto acadêmico. Contribuições, issues e sugestões são bem-vindas!
