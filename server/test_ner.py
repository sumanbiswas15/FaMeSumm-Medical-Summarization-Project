import spacy

# ✅ Load multiple medical NLP models
try:
    nlp_disease = spacy.load("en_ner_bc5cdr_md")      # Best for diseases & chemicals
    nlp_general = spacy.load("en_core_sci_md")        # General medical terms
    nlp_advanced = spacy.load("en_core_sci_scibert")  # More contextual medical terms
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    exit()

# ✅ Test Medical Text
text = """Dr. Smith: The patient is a 45-year-old female undergoing laparoscopic cholecystectomy.
The gallbladder is inflamed. Administer IV Ceftriaxone. Procedure complete, patient stable."""

# Process text with all models
doc_disease = nlp_disease(text)
doc_general = nlp_general(text)
doc_advanced = nlp_advanced(text)

# ✅ Extract Medical Entities
print("\n🔹 Extracted Medical Entities:")
for ent in doc_disease.ents:
    print(f"{ent.text} - {ent.label_}")

for ent in doc_general.ents:
    print(f"{ent.text} - {ent.label_}")

for ent in doc_advanced.ents:
    print(f"{ent.text} - {ent.label_}")
