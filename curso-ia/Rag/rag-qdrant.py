# =========================
# IMPORTAÇÕES
# =========================

# Biblioteca padrão do Python para interagir com o sistema operacional
# Aqui será usada para acessar variáveis de ambiente (API keys)
import os

# Carrega variáveis de ambiente a partir de um arquivo .env
# Muito usado para evitar expor chaves sensíveis no código
from dotenv import load_dotenv

# Cliente oficial da Groq para fazer chamadas aos modelos LLM
from groq import Groq

# Classes auxiliares do Qdrant (banco vetorial)
# Distance -> define a métrica de similaridade (COSINE, EUCLIDEAN, DOT)
# PointStruct -> estrutura que representa um vetor + metadados
# VectorParams -> configura o tamanho e tipo do vetor na coleção
from qdrant_client.http.models import Distance, PointStruct, VectorParams

# Cliente principal para interagir com o Qdrant
from qdrant_client import QdrantClient

# Modelo para gerar embeddings (transforma texto em vetor numérico)
from sentence_transformers import SentenceTransformer


# =========================
# CONFIGURAÇÃO INICIAL
# =========================

# Carrega variáveis definidas no arquivo .env
# Exemplo no .env:
# GROQ_API_KEY=xxxx
load_dotenv()


# =========================
# BASE DE CONHECIMENTO
# =========================

# Lista de documentos que servirão como base para busca semântica
# Em produção isso poderia vir de PDFs, banco SQL, API, etc.
documents = [
    "Machine learning é um campo da inteligência artificial que permite que computadores aprendam padrões a partir de dados.",
    "O aprendizado de máquina dá aos sistemas a capacidade de melhorar seu desempenho sem serem explicitamente programados.",
    "Em vez de seguir apenas regras fixas, o machine learning descobre relações escondidas nos dados.",
    "Esse campo combina estatística, algoritmos e poder computacional para extrair conhecimento.",
    "O objetivo é criar modelos capazes de generalizar além dos exemplos vistos no treinamento.",
    "Aplicações de machine learning vão desde recomendações de filmes até diagnósticos médicos.",
    "Os algoritmos de aprendizado de máquina transformam dados brutos em previsões úteis.",
    "Diferente de um software tradicional, o ML adapta-se conforme novos dados chegam.",
    "O aprendizado pode ser supervisionado, não supervisionado ou por reforço, dependendo do tipo de problema.",
    "Na prática, machine learning é o motor que impulsiona muitos avanços em visão computacional e processamento de linguagem natural.",
    "Mais do que encontrar padrões, o machine learning ajuda a tomar decisões baseadas em evidências.",
]


# =========================
# MODELO DE EMBEDDING
# =========================

# Carrega modelo pré-treinado que converte texto em vetores numéricos
# Esse modelo gera embeddings de 384 dimensões
model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# CLIENTE LLM (GROQ)
# =========================

# Inicializa cliente da Groq usando a chave do ambiente
# Permite fazer chamadas para o modelo LLM
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================
# CONFIGURAÇÃO DO QDRANT (BANCO VETORIAL)
# =========================

# Inicializa o Qdrant localmente salvando dados em disco
# Se fosse ":memory:" os dados seriam apagados ao encerrar o programa
# qdrant = QdrantClient(":memory:")
qdrant = QdrantClient(path="db/data")

# Obtém automaticamente o tamanho do vetor gerado pelo modelo
vector_size = model.get_sentence_embedding_dimension()

# Cria uma coleção no Qdrant chamada "ml_documents"
# Define:
# - tamanho do vetor
# - métrica de similaridade (COSINE)
qdrant.create_collection(
    collection_name="ml_documents",
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
)


# =========================
# INDEXAÇÃO DOS DOCUMENTOS
# =========================

# Lista que armazenará os vetores no formato aceito pelo Qdrant
points = []

# Percorre todos os documentos
for idx, doc in enumerate(documents):
    # Gera embedding do documento
    embedding = model.encode(doc).tolist()

    # Cria estrutura do ponto vetorial
    # id -> identificador único
    # vector -> embedding numérico
    # payload -> metadados (armazenamos o texto original)
    point = PointStruct(id=idx, vector=embedding, payload={"text": doc})

    points.append(point)

# Envia (insere/atualiza) os vetores na coleção
# wait=True garante que a operação finalize antes de continuar
qdrant.upsert(collection_name="ml_documents", points=points, wait=True)


# =========================
# RETRIEVER (BUSCA SEMÂNTICA)
# =========================


def retrieve(query, top_k=3):
    # Converte a pergunta do usuário em embedding
    query_embedding = model.encode(query).tolist()

    # Consulta o Qdrant buscando os vetores mais similares
    seach_result = qdrant.query_points(
        collection_name="ml_documents",
        query=query_embedding,
        limit=top_k,  # número de resultados
        with_payload=True,  # retorna também o texto armazenado
    )

    # Retorna lista de tuplas:
    # (texto_documento, score_de_similaridade)
    return [(hit.payload["text"], hit.score) for hit in seach_result.points]


# =========================
# GERADOR (LLM)
# =========================


def generate_answer(query, retrieve_docs):
    # Concatena os documentos recuperados formando o contexto
    context = "\n".join([doc for doc, _ in retrieve_docs])

    # Faz chamada ao modelo LLM da Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um especialista em machine learning. "
                    "Use apenas o contexto fornecido para responder as perguntas."
                ),
            },
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPergunta: {query}",
            },
        ],
        temperature=0,  # reduz criatividade → resposta mais factual
    )

    # Retorna apenas o texto da resposta gerada
    return response.choices[0].message.content


# =========================
# PIPELINE RAG
# =========================


def rag(query, top_k=3):
    # 1️⃣ Recupera documentos relevantes no banco vetorial
    retrieved = retrieve(query, top_k)

    # 2️⃣ Envia os documentos como contexto para o LLM
    answer = generate_answer(query, retrieved)

    # Retorna resposta + documentos utilizados
    return answer, retrieved


# =========================
# EXECUÇÃO
# =========================

# Executa o fluxo RAG com uma pergunta exemplo
answer, docs = rag("O que é machine learning?")

# Mostra resposta gerada pelo LLM
print("Resposta:", answer)

# Mostra documentos recuperados e score de similaridade
print("Documentos recuperados:")
for doc, sim in docs:
    print(f"Documento: {doc}, Similaridade: {sim}")
