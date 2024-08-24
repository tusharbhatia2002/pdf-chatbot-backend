import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

def generate_ai_response(prompt: str, context: List[Dict], db_info: Dict) -> str:
  context_str = "\n".join([f"Source: {item['metadata']['source']}\nContent: {item['text']}" for item in context])
  
  full_prompt = f"""
User Query: {prompt}

Context Information:
{context_str}

Database Information:
Surveys: {db_info['surveys']}
Responses: {db_info['responses']}

Instructions:
1. Use the provided Context Information (which includes PDF content) and Database Information to answer the query.
2. If the query is about PDF content, focus on the relevant parts of the Context Information.
3. If the query is about survey data, look for the relevant information in the Database Information.
4. If asked about specific survey or question IDs, check if they exist in the database information before answering.
5. If the requested information is not available, explain what data is available and why the specific request can't be fulfilled.
6. If the message is like "Hello" or any other greeting messages, reply accordingly"

Please provide a response based on these instructions:
"""

  try:
      model = genai.GenerativeModel('gemini-pro')
      response = model.generate_content(full_prompt)
      return response.text
  except Exception as e:
      return f"An error occurred while generating the AI response: {str(e)}"