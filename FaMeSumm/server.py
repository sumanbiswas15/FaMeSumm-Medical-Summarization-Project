import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
import spacy

# Load SciSpacy medical NER model
nlp = spacy.load("en_ner_bc5cdr_md")  # You can change this to another model if needed

# Proper model + tokenizer loading to avoid weight warnings
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to frontend URL if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input request model
class SummarizationRequest(BaseModel):
    text: str

# Define response format
class SummarizationResponse(BaseModel):
    Patient_Info: str
    Diagnosis: str
    Procedure: str
    Medications: str
    Summary: str

# Function to extract medical entities
def extract_medical_entities(text):
    doc = nlp(text)
    diagnosis = []
    procedures = []
    medications = []

    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "DISORDER"]:
            diagnosis.append(ent.text)
        elif ent.label_ in ["PROCEDURE"]:
            procedures.append(ent.text)
        elif ent.label_ in ["CHEMICAL", "MEDICATION"]:
            medications.append(ent.text)

    return {
        "Diagnosis": ", ".join(set(diagnosis)) if diagnosis else "Not specified",
        "Procedure": ", ".join(set(procedures)) if procedures else "Not specified",
        "Medications": ", ".join(set(medications)) if medications else "None prescribed"
    }

# API endpoint for medical summarization
@app.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(request: SummarizationRequest):
    try:
        text = request.text

        # Extract medical entities
        extracted_info = extract_medical_entities(text)

        # Generate a summary
        summary_result = summarizer(text, max_length=100, min_length=30, do_sample=False)
        summary_text = summary_result[0]["summary_text"]

        # Build final structured response
        response = {
            "Patient_Info": "Unknown",  # Placeholder for patient info
            "Diagnosis": extracted_info["Diagnosis"],
            "Procedure": extracted_info["Procedure"],
            "Medications": extracted_info["Medications"],
            "Summary": summary_text
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
