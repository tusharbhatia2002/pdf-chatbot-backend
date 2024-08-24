# ChatBuddy - Backend

## Overview
ChatBuddy's backend is built using FastAPI and provides the necessary APIs for handling PDF uploads, chat interactions, and data retrieval from a SQLite database.

## Features
- **PDF Uploading**: API endpoint to upload PDF files and extract their content.
- **Chat API**: Endpoint for sending user messages and receiving responses from the chatbot.
- **Key Points Extraction**: API to extract key points from uploaded PDFs.
- **Survey Data Management**: APIs to manage and retrieve survey data.

## Technologies Used
- **FastAPI**: For building the web APIs.
- **SQLite**: For storing survey data and responses.
- **SQLAlchemy**: For ORM and database interactions.
- **PyPDF2**: For extracting text from PDF files.
- **FAISS**: For efficient similarity search and retrieval of vector representations of PDF content.
- **Sentence Transformer**: For generating embeddings of text data to facilitate the vector search.

## Installation
1. Clone the repository:
bash
git clone <repository-url>
cd backend


2. Create a virtual environment and activate it:
bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate


3. Install dependencies:
bash
pip install -r requirements.txt


4. Start the FastAPI server:
bash
uvicorn main:app --reload


5. Open your browser and navigate to `http://localhost:8000/docs` to access the API documentation.

## API Endpoints
- **POST /upload-pdf/**: Upload a PDF file.
- **POST /chat/**: Send a message to the chatbot.
- **POST /extract-key-points/**: Extract key points from a specified PDF.
- **GET /pdf-files/**: Retrieve a list of uploaded PDFs.
- **DELETE /delete-pdf/{filename}**: Delete a specified PDF.
