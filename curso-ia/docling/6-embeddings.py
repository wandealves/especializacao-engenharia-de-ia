# Biblioteca padrão para manipular JSON
import json

# Classe para manipulação segura de caminhos de arquivos
from pathlib import Path

# Chunker híbrido (estrutura + limite real de tokens)
from docling.chunking import HybridChunker

# Conversor principal de documentos (PDF → documento estruturado)
from docling.document_converter import DocumentConverter

# Tokenizer compatível com HuggingFace para contagem real de tokens
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

# Cliente oficial do Qdrant (banco vetorial)
from qdrant_client import QdrantClient, models

# Biblioteca para carregar tokenizer do modelo de embedding
from transformers import AutoTokenizer


# ================================
# CONFIGURAÇÕES
# ================================

# Modelo usado para gerar embeddings
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Número máximo de tokens por chunk
MAX_TOKENS = 300


# ================================
# CONVERSÃO DO PDF
# ================================

# Instancia o conversor
converter = DocumentConverter()

# Define caminho do PDF local
pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Converte PDF em documento estruturado
result = converter.convert(pdf_path)

# Extrai objeto document
document = result.document


# ================================
# CONFIGURAÇÃO DO TOKENIZER
# ================================

tokenizer = HuggingFaceTokenizer(
    tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME),

    # Limite máximo por chunk
    max_tokens=MAX_TOKENS,

    # Limite máximo suportado pelo modelo
    model_max_length=512,

    # Se ultrapassar, corta automaticamente
    truncation=True,
)


# ================================
# CHUNKING DO DOCUMENTO
# ================================

chuncker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)

# Gera lista de chunks
chunks = list(chuncker.chunk(document))


# ================================
# LEITURA DO METADATA EXTRAÍDO
# ================================

# Valores padrão caso não encontre
paper_title = "N/A"
paper_url = "N/A"

# Caminho para o arquivo JSONL gerado anteriormente
metadata_path = (
    Path(__file__).parent.parent / "test_output" / "docling_paper_metadata.jsonl"
)

# Abre o arquivo e lê linha por linha
with open(metadata_path, "r") as f:
    for line in f:
        doc = json.loads(line)

        # Percorre as extrações feitas pelo LLM
        for extraction in doc.get("extractions", []):
            extraction_class = extraction.get("extraction_class", "")
            extraction_text = extraction.get("extraction_text", "")

            # Se for título e ainda não foi definido
            if extraction_class == "title" and paper_title == "N/A":
                paper_title = extraction_text

            # Se for URL e ainda não foi definido
            if extraction_class == "url" and paper_url == "N/A":
                paper_url = extraction_text


# Metadados que serão associados a todos os chunks
metadata_document_info = {
    "title": paper_title,
    "url": paper_url,
}


# ================================
# CONFIGURAÇÃO DO QDRANT
# ================================

# Inicializa banco vetorial local (armazenado em db/data)
qdrant = QdrantClient(path="db/data")

# Cria coleção vetorial
qdrant.create_collection(
    collection_name="docling_paper",
    vectors_config=models.VectorParams(
        # Define tamanho do vetor baseado no modelo
        size=qdrant.get_embedding_size(MODEL_NAME),

        # Métrica de similaridade (Cosine é padrão para embeddings)
        distance=models.Distance.COSINE,
    ),
)


# ================================
# PREPARAÇÃO DOS DADOS
# ================================

payload = []  # Metadados + texto
embed = []    # Documentos para embedding automático
ids = []      # IDs únicos

for idx, chunk in enumerate(chunks):

    # Payload = informação que ficará associada ao vetor
    payload.append({
        "text": chunk.text,
        "metadata": metadata_document_info
    })

    # Documento que o Qdrant usará para gerar embedding automaticamente
    embed.append(
        models.Document(
            text=chunk.text,
            model=MODEL_NAME
        )
    )

    # ID único para cada chunk
    ids.append(idx)


# ================================
# UPLOAD PARA O BANCO VETORIAL
# ================================

qdrant.upload_collection(
    collection_name="docling_paper",
    vectors=embed,
    ids=ids,
    payload=payload,
)


# ================================
# CONSULTA SEMÂNTICA
# ================================

# Faz uma pergunta em linguagem natural
result = qdrant.query_points(
    collection_name="docling_paper",
    query=models.Document(
        text="what is docling?",
        model=MODEL_NAME,
    ),
).points


# ================================
# EXIBINDO RESULTADO
# ================================

print("payload:", result[0].payload)
print("text:", result[0].payload["text"])
print("metadata:", result[0].payload["metadata"]["url"])


# Fecha conexão com o banco
qdrant.close()
