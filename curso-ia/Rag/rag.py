# Biblioteca padrão para acessar variáveis de ambiente
import os

# Biblioteca para operações matemáticas (vetores, norma, produto escalar)
import numpy as np

# Carrega variáveis de ambiente a partir de um arquivo .env
from dotenv import load_dotenv

# Cliente oficial da Groq para usar modelos LLM
from groq import Groq

# Modelo para gerar embeddings (vetores numéricos de texto)
from sentence_transformers import SentenceTransformer


# Carrega as variáveis definidas no arquivo .env
# Exemplo: GROQ_API_KEY=sua_chave
load_dotenv()


# Base de documentos que será usada como "base de conhecimento"
# Em um cenário real, isso poderia vir de banco de dados, PDFs, etc.
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


# Carrega um modelo pré-treinado de embeddings
# Esse modelo transforma texto em vetores numéricos
model = SentenceTransformer("all-MiniLM-L6-v2")

# Inicializa o cliente da Groq usando a API KEY
# A chave deve estar definida na variável de ambiente GROQ_API_KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Gera embeddings para todos os documentos da base
# Isso é feito uma única vez (pré-processamento)
doc_embeddings = model.encode(documents)


# Função para calcular similaridade de cosseno entre dois vetores
# Mede o quão parecidos dois textos são semanticamente
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Função de recuperação (Retriever)
# Recebe uma pergunta e retorna os top_k documentos mais similares
def retrieve(query, top_k=3):
    
    # Converte a pergunta em embedding
    query_embedding = model.encode([query])[0]

    similarities = []

    # Calcula a similaridade da pergunta com cada documento
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_embedding, doc_emb)
        similarities.append((i, sim))

    # Ordena os documentos pela similaridade (maior primeiro)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Retorna apenas os top_k mais relevantes
    return [(documents[i], sim) for i, sim in similarities[:top_k]]


# Função responsável por gerar a resposta usando o LLM
def generate_answer(query, retrieve_docs):

    # Junta os documentos recuperados em um único contexto
    context = "\n".join([doc for doc, _ in retrieve_docs])

    # Faz chamada ao modelo da Groq (LLM)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Modelo LLM utilizado
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em machine learning. Use apenas o contexto fornecido para responder as perguntas.",
            },
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPergunta: {query}",
            },
        ],
        temperature=0,  # Determinístico (menos criativo, mais preciso)
    )

    # Retorna apenas o texto da resposta
    return response.choices[0].message.content


# Função principal do RAG
# Orquestra recuperação + geração
def rag(query, top_k=3):

    # Recupera documentos relevantes
    retrieved = retrieve(query, top_k)

    # Gera resposta com base nesses documentos
    answer = generate_answer(query, retrieved)

    return answer, retrieved


# Executa o pipeline RAG com uma pergunta de exemplo
answer, docs = rag("O que é machine learning?")

# Exibe a resposta final
print("Resposta:", answer)

# Mostra quais documentos foram usados como contexto
print("Documentos recuperados:")
for doc, sim in docs:
    print(f"Documento: {doc}, Similaridade: {sim}")
