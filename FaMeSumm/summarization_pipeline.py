import spacy
import re
from transformers import pipeline

# Load SciSpacy medical model
nlp = spacy.load("en_core_sci_md")

# Load T5 summarization model
summarizer = pipeline("summarization", model="t5-large", framework="pt")

# Backup lists for missing terms
PROCEDURE_KEYWORDS = ["X-ray", "MRI", "CT scan", "angiogram", "biopsy", "ultrasound", "bronchoscopy", "endoscopy"]
MEDICATION_KEYWORDS = ["furosemide", "spironolactone", "carvedilol", "ceftriaxone", "azithromycin", "insulin"]
DIAGNOSIS_KEYWORDS = ["coronary artery disease", "CAD", "diabetes", "chronic kidney disease", "CKD", "hypertension",
                      "heart failure", "HFrEF", "pneumonia", "COPD", "stroke", "sepsis", "asthma", "myocardial infarction"]

def extract_medical_entities(text):
    """
    Extracts diagnoses, procedures, and medications using SciSpacy with regex backup.
    """
    doc = nlp(text)

    # Extract Patient Age & Gender
    age_match = re.search(r'(\d+)-year-old (male|female)', text, re.IGNORECASE)
    patient_info = age_match.group() if age_match else "Unknown"

    # Extract Diagnoses using SciSpacy
    diagnoses = set(ent.text for ent in doc.ents if ent.label_ in ["DISEASE", "CONDITION"])
    # Backup: Regex-based keyword matching
    diagnoses.update(re.findall(r"\b(" + "|".join(DIAGNOSIS_KEYWORDS) + r")\b", text, re.IGNORECASE))

    # Extract Procedures using SciSpacy
    procedures = set(ent.text for ent in doc.ents if ent.label_ == "PROCEDURE")
    # Backup: Regex-based keyword matching
    procedures.update(re.findall(r"\b(" + "|".join(PROCEDURE_KEYWORDS) + r")\b", text, re.IGNORECASE))

    # Extract Medications using SciSpacy
    medications = set(ent.text for ent in doc.ents if ent.label_ == "DRUG")
    # Backup: Regex-based keyword matching
    medications.update(re.findall(r"\b(" + "|".join(MEDICATION_KEYWORDS) + r")\b", text, re.IGNORECASE))

    return {
        "Patient_Info": patient_info,
        "Diagnosis": list(diagnoses) if diagnoses else ["Not specified"],
        "Procedure": list(procedures) if procedures else ["Not specified"],
        "Medications": list(medications) if medications else ["Not specified"]
    }

def generate_summary(text: str, max_length=100, min_length=50):
    """
    Generate a summary of the input medical text and extract key entities.
    """
    formatted_text = "summarize: " + text  # Required for T5 model
    result = summarizer(formatted_text, max_length=max_length, min_length=min_length, do_sample=False)
    summary = result[0]['summary_text']

    # Extract structured medical information
    medical_entities = extract_medical_entities(text)

    return {
        "Summary": summary,
        **medical_entities  # Merge extracted fields into response
    }
