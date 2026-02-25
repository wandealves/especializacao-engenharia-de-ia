import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastembed import TextEmbedding, SparseTextEmbedding
from qdrant_client import QdrantClient, models

load_dotenv()

DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SPARSE_MODEL = "Qdrant/bm25"
COLLECTION_NAME = "financial"
FILE_PATH = Path(__file__).parent / "AAPL_10-K_1A_temp.md"

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

qdrant.delete_collection(
    collection_name=COLLECTION_NAME,
)
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "dense": models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        ),
    },
    sparse_vectors_config={"sparse": models.SparseVectorParams()},
)

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

paragraphs = content.split("\n\n")
chuncks = [p.strip() for p in paragraphs if len(p.strip()) > 50]

dense_model = TextEmbedding(DENSE_MODEL)
sparce_model = SparseTextEmbedding(SPARSE_MODEL)

points = []
for i, chunk in enumerate(chuncks):
    dense_embedding = list(dense_model.passage_embed(chunk))[0].tolist()
    sparse_embedding = list(sparce_model.passage_embed(chunk))[0].as_object()
    point = models.PointStruct(
        id=str(uuid.uuid4()),
        vector={
            "dense": dense_embedding,
            "sparse": sparse_embedding,
        },
        payload={
            "text": chunk,
            "source": FILE_PATH,
        },
    )
    points.append(point)

qdrant.upload_points(
    collection_name=COLLECTION_NAME,
    points=points,
)

query_text = "What are the main financial risks?"
query_dense = list(dense_model.passage_embed(query_text))[0].tolist()
query_sparse = list(sparce_model.passage_embed(query_text))[0].as_object()

print("Query Dense", query_dense)
print("Query Sparse", query_sparse)

results = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    prefetch=[
        {"query": query_dense, "using": "dense", "limit": 10},
        {"query": query_sparse, "using": "sparse", "limit": 10},
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=3,
)

for result in results.points:
    print(f"Score: {result.score}")
    print(f"Text: {result.payload['text'][:100]}...")
    print("-" * 80)
