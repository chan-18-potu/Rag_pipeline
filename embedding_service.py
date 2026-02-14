# embedding_service.py
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def embed_texts(texts):
    return model.encode(texts, convert_to_numpy=True)
