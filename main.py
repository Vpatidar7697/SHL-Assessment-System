from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import uvicorn

app = FastAPI()

# 1. Database load karein (HF par RAM zyada hai, isliye direct load karein)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector DB load karein
vector_db = Chroma(persist_directory="./shl_vector_db", embedding_function=embeddings)

# Request format define karein
class QueryRequest(BaseModel):
    query: str

# 2. Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 3. Recommendation Endpoint
@app.post("/recommend")
def recommend_assessment(request: QueryRequest):
    # Search logic: Top 10 results
    results = vector_db.similarity_search(request.query, k=10)
    
    recommended = []
    for doc in results:
        recommended.append({
            "url": doc.metadata.get("url", "N/A"),
            "name": doc.metadata.get("name", "N/A"),
            "description": doc.page_content[:200] + "...", 
            "test_type": [doc.metadata.get("test_type", "General")]
        })
    
    return {"recommended_assessments": recommended}

# 4. Hugging Face Port Binding (7860)
if __name__ == "__main__":
    # HF default port 7860 mangta hai
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
