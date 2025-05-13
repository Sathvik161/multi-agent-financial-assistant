from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_DIR = "data/filings"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists

# Initialize with empty index
dimension = 384  # Dimension of 'all-MiniLM-L6-v2' embeddings
index = faiss.IndexFlatL2(dimension)
documents = []
metadata = []

def initialize_retriever():
    """Initialize or update the FAISS index with documents"""
    global index, documents, metadata
    
    # Load documents from files
    new_docs = []
    new_meta = []
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith((".txt", ".md")):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():  # Only add non-empty documents
                    new_docs.append(content)
                    new_meta.append({"source": filename})
    
    if new_docs:
        # Create embeddings for new documents
        new_embeddings = model.encode(new_docs)
        
        # Update index and metadata
        if documents:
            # Append to existing index
            index.add(np.array(new_embeddings))
            documents.extend(new_docs)
            metadata.extend(new_meta)
        else:
            # Create new index
            index = faiss.IndexFlatL2(new_embeddings.shape[1])
            index.add(np.array(new_embeddings))
            documents = new_docs
            metadata = new_meta

# Initialize on startup
initialize_retriever()

@app.get("/retrieve")
def retrieve(
    query: str = Query(...),
    k: int = Query(3, ge=1, le=10)
):
    try:
        if not documents:
            raise HTTPException(
                status_code=404,
                detail="No documents available for retrieval. Please add documents to data/filings first."
            )
            
        query_vec = model.encode([query])
        distances, indices = index.search(query_vec, k)
        
        results = []
        for i in indices[0]:
            if i < 0:  # Handle cases where FAISS returns invalid indices
                continue
            results.append({
                "source": metadata[i]["source"],
                "content": documents[i],
                "distance": float(distances[0][i])
            })
            
        return {
            "query": query,
            "results": results[:k]  # Ensure we return no more than k results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
def refresh_index():
    """Force refresh of the document index"""
    try:
        initialize_retriever()
        return {
            "status": "success",
            "documents_loaded": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))