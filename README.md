# 📄 AI PDF Query System

An AI-powered PDF Question Answering system built with **FastAPI**, **Gemini (Google)**, **AWS (S3, Lambda, DynamoDB)**, and **FAISS**. Users can upload PDFs, which are embedded, stored, and then queried with natural language using Gemini 1.5 Flash.

---

## 🚀 Features

- 📤 Upload PDFs and store them on **AWS S3**
- 📑 Extract and chunk PDF text using **PyPDF2**
- 🔎 Embed text using **Sentence Transformers** and **FAISS**
- 💡 Ask natural language questions answered by **Gemini 1.5 Flash**
- 🧠 Store metadata in **DynamoDB**
- 📈 Invoke an **AWS Lambda** function to log query metrics
- 🌐 Frontend UI with HTML + JavaScript for user interaction

---

## 🧰 Tech Stack

| Layer       | Tools/Tech                          |
|-------------|-------------------------------------|
| Backend     | FastAPI, Python                     |
| Embedding   | SentenceTransformers (`MiniLM-L6`)  |
| Search      | FAISS                               |
| LLM         | Gemini 1.5 Flash (via Google GenAI) |
| Cloud       | AWS S3, Lambda, DynamoDB            |
| Frontend    | HTML + JS                           |

---

## 🗂️ Project Structure    
├── main.py # FastAPI application  
├── web/ # Frontend HTML  
├── modules/  
│ ├── pdf_loader.py # PDF text extraction  
│ ├── embedder.py # Text chunking + embedding  
│ ├── query_engine.py # Gemini-based answer generation  
│ ├── s3_uploader.py # Upload to AWS S3  
│ ├── dynamo_store.py # Save metadata to DynamoDB  
│ └── gemini_service.py # Google Gemini API setup  
└── temp/ # Temporary uploaded PDF storage  


---

## ⚙️ Setup Instructions

### 1. ✅ Clone the Repo

```bash
git clone https://github.com/Siva-Sakthii/rag-project-penteai.git
cd rag-project-penteai
```
### 2. 🧪 Create Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. 📦 Install Dependencies
```
pip install -r requirements.txt
```

### 4. 🔐 Setup Environment Variables
Create a .env file in the root directory:
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=ap-south-1
GOOGLE_API_KEY=your_gemini_api_key
```
### 5. 🛠️ AWS Configuration
Ensure the following AWS services are ready:  

✅ S3 Bucket: Create a bucket and update BUCKET_NAME in s3_uploader.py  

✅ DynamoDB Table: Table named PDFMetadata with id as primary key  

✅ Lambda Function: Named storeLLMMetrics (used for logging query info)  

### 6. ▶️ Run the App

```
uvicorn main:app --reload
```
  
Visit: http://127.0.0.1:8000/web/index.html
  
## 🧪 How It Works
- Upload PDF → Stored in temp/ → Uploaded to S3
- Text Extraction → PDF parsed and split into 500-char chunks
- Embedding → FAISS index built using SentenceTransformer
- Query → User asks a question → Nearest chunks selected
- Gemini → Context and question sent to Gemini API → Answer generated
- Metadata → PDF info stored in DynamoDB, Lambda logs query
  
## 📷 UI Preview

> ![PDF Query UI](https://github.com/Siva-Sakthii/rag-project-penteai/blob/main/web/img_1.jpg)  
> _Simple interface to upload and query PDFs_


## ✅ Example Query
- Upload a syllabus or research paper PDF
- Ask: What is the main topic of this document?
- The system returns a Gemini-generated answer using embedded chunks.
  
## 👩‍💻 Author
Siva Sakthii U S  
B.Tech - AI & ML  
Sri Shakthi Institute of Engineering & Technology  
