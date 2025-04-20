from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from summarization_pipeline import generate_summary  # Import the summarization function

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

# Request model for summarization
class SummarizationRequest(BaseModel):
    text: str
    max_length: int = 100  # Adjusted for better summaries
    min_length: int = 50

@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    """
    API endpoint to summarize medical text and extract structured data.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")

    summary_data = generate_summary(request.text, max_length=request.max_length, min_length=request.min_length)

    return summary_data  # Return structured summary + extracted medical entities
