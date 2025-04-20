from huggingface_hub import hf_hub_download
import os

# Download the model file from the correct repo
file_path = hf_hub_download(
    repo_id="allenai/en_ner_bc5cdr_md",
    filename="en_ner_bc5cdr_md-0.5.0.tar.gz",
    repo_type="model"
)

# Install the model
os.system(f"pip install {file_path}")
