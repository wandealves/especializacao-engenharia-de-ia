import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models

load_dotenv()

MODEL_MANE = "sentence-transformers/all-MiniLM-L6-v2"
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
    vectors_config=models.VectorParams(
        size=384,
        distance=models.Distance.COSINE,
    ),
)

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

paragraphs = content.split("\n\n")
chuncks = [p.strip() for p in paragraphs if len(p.strip()) > 50]

model = TextEmbedding(MODEL_MANE)

points = []
for i, chunk in enumerate(chuncks):
    embedding = list(model.passage_embed(chunk))[0].tolist()
    point = models.PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
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
query_embedding = list(model.passage_embed(query_text))[0].tolist()
results = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding,
    limit=3,
)

for result in results.points:
    print(f"Score: {result.score}")
    print(f"Text: {result.payload['text'][:100]}...")
    print("-" * 80)
