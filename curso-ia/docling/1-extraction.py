# Importa a classe Path da biblioteca padrão pathlib
# Ela facilita o trabalho com caminhos de arquivos de forma segura e multiplataforma
from pathlib import Path

# Importa o DocumentConverter da biblioteca docling
# Essa classe é responsável por converter documentos (PDF, URL, etc.)
# para um formato estruturado manipulável em Python
from docling.document_converter import DocumentConverter

# Cria uma instância do conversor
# A partir dela poderemos chamar o método convert()
converter = DocumentConverter()

# ================================
# EXEMPLO USANDO ARQUIVO LOCAL
# ================================

# Cria o caminho do arquivo PDF local
# __file__ representa o arquivo Python atual
# .parent pega a pasta onde o script está
# / "2408.09869v5.pdf" adiciona o nome do PDF ao caminho
# pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Converte o PDF local para o formato interno do Docling
# result = converter.convert(pdf_path)


# ================================
# EXEMPLO USANDO PDF VIA URL
# ================================

# Converte diretamente o PDF disponível na internet (arXiv)
# O Docling baixa o arquivo e faz a conversão automaticamente
result = converter.convert("https://arxiv.org/pdf/2408.09869")

# O objeto result contém várias informações da conversão
# Aqui acessamos o documento estruturado convertido
document = result.document

# Exporta o conteúdo do documento convertido para o formato Markdown
# Isso transforma o PDF em texto estruturado com marcações (títulos, listas, etc.)
markdown_output = document.export_to_markdown()

# Imprime o conteúdo em Markdown no terminal
print(markdown_output)
