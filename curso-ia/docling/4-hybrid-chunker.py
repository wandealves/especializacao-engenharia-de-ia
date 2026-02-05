# Classe para manipulação de caminhos de arquivos (forma segura e multiplataforma)
from pathlib import Path

# HybridChunker → estratégia de chunking que combina
# estrutura hierárquica + limite de tokens
from docling.chunking import HybridChunker

# Conversor principal do Docling (transforma PDF em documento estruturado)
from docling.document_converter import DocumentConverter

# Wrapper de tokenizer compatível com o sistema de chunking do Docling
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

# Biblioteca da Hugging Face para carregar tokenizers pré-treinados
from transformers import AutoTokenizer

# ================================
# CONFIGURAÇÕES
# ================================

# Modelo que será usado para gerar embeddings
# Aqui usamos um modelo pequeno e eficiente
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Número máximo de tokens por chunk
# Isso é importante para:
# - não ultrapassar limite do modelo
# - manter consistência no embedding
MAX_TOKENS = 300


# ================================
# CONVERSÃO DO PDF
# ================================

# Instancia o conversor
converter = DocumentConverter()

# Define o caminho do PDF local
# __file__ → arquivo Python atual
# .parent → diretório onde o script está
pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Converte o PDF para um documento estruturado
result = converter.convert(pdf_path)

# Extrai o objeto document do resultado
document = result.document


# ================================
# CONFIGURAÇÃO DO TOKENIZER
# ================================

# Cria o tokenizer baseado no modelo de embedding escolhido
# AutoTokenizer baixa automaticamente o tokenizer do modelo
tokenizer = HuggingFaceTokenizer(
    tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL),
    # Define o limite máximo de tokens permitido
    max_tokens=MAX_TOKENS,
)


# ================================
# CONFIGURAÇÃO DO HYBRID CHUNKER
# ================================

# O HybridChunker combina:
# - Estrutura hierárquica do documento
# - Limite real de tokens baseado no tokenizer

chuncker = HybridChunker(
    tokenizer=tokenizer,  # tokenizer usado para contar tokens reais
    max_tokens=MAX_TOKENS,  # limite máximo por chunk
    merge_peers=True,  # permite unir blocos do mesmo nível estrutural
)


# ================================
# GERAÇÃO DOS CHUNKS
# ================================

# Aplica o chunker ao documento
# Retorna um gerador → convertendo para lista para facilitar uso
chuncks = list(chuncker.chunk(document))


# ================================
# EXIBIÇÃO DOS CHUNKS
# ================================

# Percorre todos os chunks gerados
for i, chunk in enumerate(chuncks):
    # Imprime o índice do chunk
    print(f"--- Chunk {i} ---\n")

    # Conta quantos tokens reais existem no texto do chunk
    txt_tokens = tokenizer.count_tokens(chunk.text)

    # Exibe:
    # - número de tokens
    # - conteúdo textual do chunk
    print(f"chunck_text: ({txt_tokens} tokens):\n{chunk.text}!r")

    print()
