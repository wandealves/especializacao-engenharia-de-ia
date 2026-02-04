# Biblioteca padrão para interagir com o sistema operacional
# Aqui será usada para criar diretórios
import os

# Classe para manipulação de caminhos de arquivos de forma segura
from pathlib import Path

# Enum que define os formatos de entrada suportados (PDF, DOCX, etc.)
from docling.datamodel.base_models import InputFormat

# Opções específicas do pipeline de processamento de PDF
# Permite configurar como o PDF será interpretado
from docling.datamodel.pipeline_options import PdfPipelineOptions

# DocumentConverter é o conversor principal
# PdfFormatOption permite configurar opções específicas para PDF
from docling.document_converter import DocumentConverter, PdfFormatOption

# Classe que representa imagens encontradas dentro do documento
from docling_core.types.doc import PictureItem

# ================================
# CONFIGURAÇÃO DO PIPELINE PDF
# ================================

# Cria um objeto de configuração para processamento de PDF
pipeline_options = PdfPipelineOptions()

# Define a escala das imagens extraídas
# 2.0 significa que as imagens serão renderizadas com o dobro da resolução padrão
pipeline_options.images_scale = 2.0

# Habilita a geração de imagens para elementos gráficos encontrados no PDF
pipeline_options.generate_picture_images = True


# ================================
# CONFIGURAÇÃO DO CONVERTER
# ================================

# Cria o DocumentConverter configurando explicitamente
# que quando o formato for PDF, deve usar as opções definidas acima
converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
)


# ================================
# CONVERSÃO DO PDF
# ================================

# Define o caminho do PDF local
# __file__ → arquivo Python atual
# .parent → pasta onde o script está
# / "2408.09869v5.pdf" → adiciona o nome do arquivo
pdf_path = Path(__file__).parent / "2408.09869v5.pdf"

# Executa a conversão do PDF
result = converter.convert(pdf_path)


# ================================
# CRIAÇÃO DA PASTA PARA IMAGENS
# ================================

# Cria a pasta "images" se ela não existir
# exist_ok=True evita erro caso a pasta já exista
os.makedirs("images", exist_ok=True)


# ================================
# EXTRAÇÃO DAS IMAGENS DO DOCUMENTO
# ================================

# Contador para numerar as imagens extraídas
picture_counter = 0

# Itera sobre todos os elementos estruturados do documento
# iterate_items() percorre títulos, parágrafos, tabelas, imagens, etc.
for element, _level in result.document.iterate_items():
    # Verifica se o elemento atual é uma imagem (PictureItem)
    if isinstance(element, PictureItem):
        # Incrementa o contador de imagens
        picture_counter += 1

        # Define o caminho do arquivo onde a imagem será salva
        image_path = Path("images") / f"picture_{picture_counter}.png"

        # Abre o arquivo em modo binário para escrita ("wb")
        with open(image_path, "wb") as f:
            # Obtém a imagem associada ao elemento
            # e salva no formato PNG
            element.get_image(result.document).save(f, "PNG")

        # Exibe mensagem confirmando o salvamento
        print(f"Saved image to {image_path}")
