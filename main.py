import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os

from database import get_db, get_surveys, get_responses, get_survey_by_id, get_responses_by_survey_id, get_response_count_by_survey_id
import pdf_handler as pdf
import ai_handler as ai
import vector_store as vs

app = FastAPI()

# Enable CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class ChatMessage(BaseModel):
  message: str

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
  try:
      file_path = await pdf.save_pdf(file)
      text_content = pdf.extract_text_from_pdf(file_path)
      vs.add_pdf_to_vector_store(text_content, file.filename)
      return {"message": "PDF uploaded and processed successfully", "file_name": file.filename}
  except Exception as e:
      print(f"Error uploading PDF: {str(e)}")
      print(traceback.format_exc())
      raise HTTPException(status_code=500, detail=str(e))

@app.get("/pdf-files/")
async def get_pdf_files():
  return {"pdf_files": pdf.get_pdf_files()}

@app.post("/chat/")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
  try:
      context = vs.get_relevant_context(message.message)
      db_info = {
          "surveys": get_surveys(db),
          "responses": get_responses(db)
      }
      response = ai.generate_ai_response(message.message, context, db_info)
      return {"response": response}
  except Exception as e:
      print(f"Error in chat: {str(e)}")
      print(traceback.format_exc())
      raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
  try:
      db = next(get_db())
      surveys = get_surveys(db)
      responses = get_responses(db)
      
      for survey in surveys:
          survey_text = f"Survey ID: {survey.survey_id}, Question ID: {survey.question_id}, Question: {survey.question}"
          vs.add_to_vector_store(survey_text, {"source": "survey", "type": "database"})
      
      for response in responses:
          response_text = f"User ID: {response.user_id}, Survey ID: {response.survey_id}, Question ID: {response.question_id}, Response: {response.response}"
          vs.add_to_vector_store(response_text, {"source": "response", "type": "database"})

      pdf_files = pdf.get_pdf_files()
      for pdf_file in pdf_files:
          text_content = pdf.get_pdf_content(pdf_file)
          vs.add_pdf_to_vector_store(text_content, pdf_file)
      print("Startup completed successfully")
  except Exception as e:
      print(f"Error during startup: {str(e)}")
      print(traceback.format_exc())

@app.delete("/delete-pdf/{filename}")
async def delete_pdf(filename: str):
  try:
      print(f"Attempting to delete PDF: {filename}")
      file_path = pdf.get_pdf_path(filename)
      print(f"File path: {file_path}")
      
      if os.path.exists(file_path):
          os.remove(file_path)
          print(f"File removed: {file_path}")
          vs.remove_pdf_from_vector_store(filename)
          print(f"PDF removed from vector store: {filename}")
          return {"message": f"PDF {filename} deleted successfully"}
      else:
          print(f"File not found: {file_path}")
          raise HTTPException(status_code=404, detail="PDF not found")
  except Exception as e:
      print(f"Error deleting PDF: {str(e)}")
      print(traceback.format_exc())
      raise HTTPException(status_code=500, detail=str(e))
  
@app.post("/extract-key-points/")
async def extract_key_points(pdf_file: str, num_points: int = 5):
  try:
      pdf_content = pdf.get_pdf_content(pdf_file)
      key_points = ai.extract_key_points(pdf_content, num_points)
      return {"key_points": key_points}
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)