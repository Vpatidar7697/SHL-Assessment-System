from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI()

# 1. Database load karein
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./shl_vector_db", embedding_function=embeddings)

# Request format define karein
class QueryRequest(BaseModel):
    query: str

# 2. Health Check Endpoint [cite: 155]
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 3. Recommendation Endpoint [cite: 163]
@app.post("/recommend")
def recommend_assessment(request: QueryRequest):
    # Search logic: Top 10 results nikaalein [cite: 163]
    results = vector_db.similarity_search(request.query, k=10)
    
    recommended = []
    for doc in results:
        recommended.append({
            "url": doc.metadata.get("url", "N/A"),
            "name": doc.metadata.get("name", "N/A"),
            "description": doc.page_content[:200] + "...", # Pehle 200 words
            "test_type": [doc.metadata.get("test_type", "General")]
        })
    
    return {"recommended_assessments": recommended}