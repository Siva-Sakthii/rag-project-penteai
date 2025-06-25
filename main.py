from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import traceback
import boto3
import json

from modules.pdf_loader import extract_text
from modules.embedder import embed_text, build_index, _model
from modules.query_engine import generate_answer
from modules.s3_uploader import upload_file_to_s3
from modules.dynamo_store import save_pdf_metadata

# ------------------------ App Setup ------------------------
app = FastAPI()
storage = {}

# Ensure AWS credentials exist
assert os.getenv("AWS_ACCESS_KEY_ID"), "❌ Missing AWS_ACCESS_KEY_ID"
assert os.getenv("AWS_SECRET_ACCESS_KEY"), "❌ Missing AWS_SECRET_ACCESS_KEY"
assert os.getenv("AWS_REGION"), "❌ Missing AWS_REGION"

# Create required folders
os.makedirs("temp", exist_ok=True)

# Mount frontend folder
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# Initialize Lambda client
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# ---------------------- Upload PDF ----------------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs allowed")

        path = f"./temp/{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        print(f"📥 Saved: {path}")

        # Upload to S3
        s3_key = f"uploads/{file.filename}"
        s3_url = upload_file_to_s3(path, s3_key)
        if not s3_url:
            raise HTTPException(status_code=500, detail="S3 upload failed")
        print(f"✅ S3 URL: {s3_url}")

        # Process text
        text = extract_text(path)
        chunks, embs = embed_text(text)
        index = build_index(embs)
        storage['chunks'] = chunks
        storage['index'] = index
        print(f"🔍 Embedded {len(chunks)} chunks")

        # Save metadata
        save_pdf_metadata(file.filename, s3_url, len(chunks))

        return {
            "message": "✅ PDF processed and stored",
            "filename": file.filename,
            "chunks": len(chunks),
            "s3_url": s3_url
        }

    except Exception as e:
        print("🔥 Upload Error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ---------------------- Query ----------------------
@app.post("/query")
async def query(q: str = Form(...)):
    if 'index' not in storage:
        raise HTTPException(status_code=400, detail="Please upload a PDF first.")
    try:
        # Encode query
        q_emb = _model.encode([q]).astype('float32')
        D, I = storage['index'].search(q_emb, k=3)
        selected = "\n\n".join(storage['chunks'][i] for i in I[0])

        # Generate response
        ans = generate_answer(q, selected)

        # Send metrics to Lambda (corrected payload)
        payload = {
            "query": q,
            "answer": ans,
            "source": "pdf_query_app"
        }

        response = lambda_client.invoke(
                FunctionName="storeLLMMetrics",
                InvocationType="Event",
                Payload=json.dumps({
                        "question": q,
                        "answer": ans,
                        "source": "pdf_query_app"
                    })
                )

        print("📊 Lambda invoked:", response['StatusCode'])
        
        return {"answer": ans}

    except Exception as e:
        print("❌ Query Error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process query")
