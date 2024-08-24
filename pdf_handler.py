import os
import PyPDF2
from fastapi import UploadFile
from typing import List

PDF_DIRECTORY = "./pdfs/"

def ensure_pdf_directory():
  if not os.path.exists(PDF_DIRECTORY):
      os.makedirs(PDF_DIRECTORY)

async def save_pdf(file: UploadFile) -> str:
  ensure_pdf_directory()
  file_path = os.path.join(PDF_DIRECTORY, file.filename)
  with open(file_path, "wb") as buffer:
      content = await file.read()
      buffer.write(content)
  return file_path

def extract_text_from_pdf(file_path: str) -> str:
  with open(file_path, 'rb') as file:
      reader = PyPDF2.PdfReader(file)
      text = ""
      for page in reader.pages:
          text += page.extract_text() + "\n"
  return text

def get_pdf_files() -> List[str]:
  ensure_pdf_directory()
  return [f for f in os.listdir(PDF_DIRECTORY) if f.endswith('.pdf')]

def get_pdf_content(filename: str) -> str:
  file_path = os.path.join(PDF_DIRECTORY, filename)
  return extract_text_from_pdf(file_path)

def get_pdf_path(filename: str) -> str:
  """Return the full path to the specified PDF file."""
  return os.path.join(PDF_DIRECTORY, filename)

def get_all_pdf_contents() -> List[str]:
  """Fetch the content of all PDFs in the directory."""
  pdf_files = get_pdf_files()  # Get the list of PDF files
  contents = []
  for pdf_file in pdf_files:
      content = get_pdf_content(pdf_file)  # Extract text from each PDF
      contents.append(content)
  return contents