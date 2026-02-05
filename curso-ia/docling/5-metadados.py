# Biblioteca padrão para interagir com variáveis de ambiente
import os

# Biblioteca para manipulação de texto multilinha
# Aqui usada para formatar o prompt corretamente
import textwrap

# Classe para trabalhar com caminhos de arquivos
from pathlib import Path

# Biblioteca LangExtract (extração estruturada via LLM)
import langextract as lx

# Conversor de documentos do Docling (PDF → documento estruturado)
from docling.document_converter import DocumentConverter

# Carrega variáveis de ambiente a partir de um arquivo .env
# Geralmente usado para armazenar API Keys
from dotenv import load_dotenv

# Provider de modelo OpenAI usado pelo LangExtract
from langextract.providers.openai import OpenAILanguageModel

# ================================
# CONFIGURAÇÃO INICIAL
# ================================

# Carrega as variáveis de ambiente (.env)
# Exemplo: OPENAI_API_KEY
load_dotenv()


# ================================
# CONVERSÃO DO PDF
# ================================

# Instancia o conversor
converter = DocumentConverter()

# Define o caminho do PDF local
pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Converte o PDF em documento estruturado
result = converter.convert(pdf_path)

# Extrai o objeto document
document = result.document

# Exporta o documento para Markdown
# Isso facilita enviar o texto para o LLM
markdown_output = document.export_to_markdown()

# Pega apenas os primeiros 6000 caracteres
# Evita enviar texto muito grande para o modelo
first_pages = markdown_output[:6000]


# ================================
# DEFINIÇÃO DO PROMPT
# ================================

# textwrap.dedent remove indentação extra do texto
# O prompt instrui o modelo a extrair metadados específicos
prompt = textwrap.dedent("""\
Extract metadata from this technical report including title, all authors, 
affiliation, version number, and GitHub repository URLs.
Use exact text from the document.
""")


# ================================
# EXEMPLO (FEW-SHOT LEARNING)
# ================================

# Criamos um exemplo de entrada e saída esperada
# Isso ajuda o modelo a entender o formato desejado

examples = [
    lx.data.ExampleData(
        text="Docling Technical Report\nVersion 1.0\nChristoph Auer Maksym Lysak Ahmed Nassar\nAI4K Group, IBM Research\nRüschlikon, Switzerland\ngithub.com/DS4SD/docling",
        # Lista de extrações esperadas para esse texto
        extractions=[
            lx.data.Extraction(
                extraction_class="title",
                extraction_text="Docling Technical Report",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="author",
                extraction_text="Christoph Auer",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="author", extraction_text="Maksym Lysak", attributes={}
            ),
            lx.data.Extraction(
                extraction_class="affiliation",
                extraction_text="AI4K Group, IBM Research",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="url",
                extraction_text="github.com/DS4SD/docling",
                attributes={"type": "repository"},
            ),
        ],
    )
]


# ================================
# EXECUÇÃO DA EXTRAÇÃO COM LLM
# ================================

# lx.extract envia:
# - o texto
# - o prompt
# - os exemplos
# - o modelo escolhido
# para o LLM realizar a extração estruturada

extraction_result = lx.extract(
    text_or_documents=first_pages,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-4o-mini",  # modelo usado para extração
)


# ================================
# SALVANDO RESULTADO
# ================================

# Salva o resultado em formato JSONL anotado
# Cada linha representa um documento com suas extrações
lx.io.save_annotated_documents(
    [extraction_result], output_name="docling_paper_metadata.jsonl"
)


# ================================
# EXIBINDO RESULTADOS
# ================================

# Linha separadora no terminal
print("-" * 80)

# Percorre todas as extrações encontradas
for extraction in extraction_result.extractions:
    # Imprime classe e texto extraído
    print(f"{extraction.extraction_class}: {extraction.extraction_text}")

    # Se houver atributos extras (ex: tipo de URL), imprime também
    if extraction.attributes:
        print(f"  Atributos: {extraction.attributes}")
