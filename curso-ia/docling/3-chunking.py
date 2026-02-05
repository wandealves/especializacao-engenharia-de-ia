# Importa a classe Path para trabalhar com caminhos de arquivos
# de forma segura e independente do sistema operacional
from pathlib import Path

# Importa o HierarchicalChunker
# Essa classe é responsável por dividir o documento em "chunks"
# (pedaços de texto) respeitando a hierarquia estrutural
# como títulos, seções, subseções etc.
from docling.chunking import HierarchicalChunker

# Importa o conversor principal de documentos do Docling
# Ele é responsável por transformar PDFs (ou outros formatos)
# em um documento estruturado manipulável em Python
from docling.document_converter import DocumentConverter

# ================================
# CONVERSÃO DO PDF
# ================================

# Cria uma instância do conversor
converter = DocumentConverter()

# Define o caminho do PDF local
# __file__ → representa o arquivo Python atual
# .parent → pasta onde o script está localizado
# / "2408.09869v5.pdf" → adiciona o nome do PDF ao caminho
pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Executa a conversão do PDF
# O resultado contém metadados e o documento estruturado
result = converter.convert(pdf_path)

# Extrai o objeto document estruturado do resultado
document = result.document


# ================================
# CHUNKING HIERÁRQUICO
# ================================

# Cria uma instância do HierarchicalChunker
# Esse chunker divide o texto respeitando a estrutura do documento
# (ex: mantém blocos organizados por seções)
chunker = HierarchicalChunker()

# Aplica o chunker ao documento
# chunk(document) retorna um gerador de chunks
# list(...) converte o gerador em uma lista para acesso por índice
chunks = list(chunker.chunk(document))


# ================================
# ACESSANDO UM CHUNK ESPECÍFICO
# ================================

# Imprime o texto do quinto chunk (índice 4, pois começa em 0)
# Cada chunk geralmente possui:
# - text → conteúdo textual
# - metadata → informações estruturais
print(chunks[4].text)
