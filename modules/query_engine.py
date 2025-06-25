from modules.embedder import _model
from modules.gemini_service import model

def generate_answer(query: str, context: str) -> str:
    prompt = f"Context:\n{context}\n\nUser question: {query}"
    resp = model.generate_content(prompt)
    return resp.text
