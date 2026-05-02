from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from inference import InferenceEngine
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="AI Multi-Tab Summarizer API")

# Enable CORS for the Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to extension ID
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the inference engine once on startup
engine = InferenceEngine()

# Data models
class TextRequest(BaseModel):
    text: str

class BatchRequest(BaseModel):
    texts: List[str]

@app.get("/")
def read_root():
    return {"message": "AI Summarizer Backend is running!"}

@app.post("/summarize_single")
def summarize_single(request: TextRequest):
    """Summarizes a single piece of text."""
    try:
        summary = engine.summarize(request.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize_batch")
def summarize_batch(request: BatchRequest):
    """
    Summarizes multiple pieces of text and provides:
    1. Individual summaries
    2. A combined summary of all inputs
    """
    try:
        # 1. Generate individual summaries
        individual_summaries = [engine.summarize(t) for t in request.texts]
        
        # 2. Generate combined summary
        # We combine the summaries (or the original texts if not too long)
        combined_text = " ".join(individual_summaries)
        final_summary = engine.summarize(combined_text)
        
        return {
            "individual_summaries": individual_summaries,
            "combined_summary": final_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
