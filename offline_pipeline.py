# offline_pipeline.py
import os
import json
import numpy as np

from config import BASE_STORAGE_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from utils import ensure_user_folders
from pdf_loader import extract_text_from_pdf
from text_processing import normalize_text, chunk_text
from embedding_service import embed_texts
from faiss_store import load_or_create_index, save_index


def process_pdf(user_id, pdf_path, document_id):
    # 1. Ensure folders
    user_path = ensure_user_folders(BASE_STORAGE_PATH, user_id)

    # 2. Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        raise ValueError("Empty PDF text")

    # 3. Normalize
    clean_text = normalize_text(raw_text)

    # 4. Chunk
    chunks = chunk_text(clean_text, CHUNK_SIZE, CHUNK_OVERLAP)

    # 5. Embed
    embeddings = embed_texts(chunks)
    embedding_dim = embeddings.shape[1]

    # 6. FAISS index
    index = load_or_create_index(embedding_dim)
    index.add(embeddings)
    save_index(index)

    # 7. Save metadata
    metadata = []
    for i, chunk in enumerate(chunks):
        metadata.append({
            "user_id": user_id,
            "document_id": document_id,
            "chunk_id": i,
            "text": chunk
        })

    metadata_path = os.path.join(user_path, "metadata", f"{document_id}.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return len(chunks)
