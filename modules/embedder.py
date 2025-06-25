from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str, chunk_size=500):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embs = _model.encode(chunks)
    return chunks, embs.astype('float32')

def build_index(embs: np.ndarray):
    idx = faiss.IndexFlatL2(embs.shape[1])
    idx.add(embs)
    return idx
