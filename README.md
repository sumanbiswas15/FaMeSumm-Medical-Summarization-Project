# FaMeSumm Medical Summarization Project

## Project Overview
FaMeSumm is a framework designed to improve the faithfulness of medical text summarization. It leverages advanced language models fine-tuned with contrastive learning and medical knowledge incorporation to generate accurate and reliable summaries of medical documents. The core FaMeSumm framework includes a FastAPI backend that provides summarization and medical entity extraction services.

This project integrates three main components:
- **FaMeSumm**: The core medical summarization framework and FastAPI backend.
- **server**: A Node.js Express backend that acts as a proxy to the FaMeSumm API, persists summaries in a MongoDB database, and exposes RESTful endpoints.
- **client**: A React frontend application built with Create React App that provides a user interface to interact with the summarization service.

## Project Structure
- `FaMeSumm/`  
  Contains the core summarization framework, training scripts, datasets, and a FastAPI backend (`server.py`) for medical summarization and entity extraction.
- `server/`  
  Node.js Express backend that connects to a MongoDB database, proxies requests to the FaMeSumm FastAPI backend, and manages summary persistence.
- `client/`  
  React frontend application providing the user interface to input medical text and view generated summaries.

## Installation

### Prerequisites
- Python 3.8+ (for FaMeSumm backend)
- Node.js and npm (for server and client)
- MongoDB (for server database)

### FaMeSumm Backend
1. Navigate to the `FaMeSumm` directory:
   ```bash
   cd FaMeSumm
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Download or prepare datasets and trained model checkpoints as described in `FaMeSumm/README.md`.

### Server Backend
1. Navigate to the `server` directory:
   ```bash
   cd ../server
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Ensure MongoDB is running locally on `mongodb://127.0.0.1:27017/medical_summaries`.

### Client Frontend
1. Navigate to the `client` directory:
   ```bash
   cd ../client
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Project

1. Start the FaMeSumm FastAPI backend:
   ```bash
   cd FaMeSumm
   uvicorn server:app --host 0.0.0.0 --port 8000
   ```
2. Start the Node.js server backend:
   ```bash
   cd ../server
   npm start
   ```
3. Start the React frontend:
   ```bash
   cd ../client
   npm start
   ```
4. Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to use the application.

## Usage
- Use the React frontend to input medical text.
- The frontend sends requests to the Node.js backend.
- The Node.js backend forwards requests to the FaMeSumm FastAPI backend for summarization and entity extraction.
- Summaries are saved in MongoDB and can be retrieved via the backend API.

## Citation and Acknowledgements
This project is based on the paper:

Zhang, Nan, et al. "FaMeSumm: Investigating and Improving Faithfulness of Medical Summarization." EMNLP 2023.  
[https://arxiv.org/abs/2311.02271](https://arxiv.org/abs/2311.02271)

Acknowledgement:  
The fine-tuning code is developed based on:  
https://github.com/priya-dwivedi/Deep-Learning/blob/master/wikihow-fine-tuning-T5/Tune_T5_WikiHow-Github.ipynb

## Additional Information
For detailed information on the FaMeSumm framework and datasets, please refer to the [FaMeSumm README](FaMeSumm/README.md).  
For details on the React frontend, see the [client README](client/README.md).

---
