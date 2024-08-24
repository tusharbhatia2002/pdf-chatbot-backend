from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # 384 is the dimensionality of the chosen model
texts = []
metadata = []

def add_to_vector_store(text: str, meta: Dict[str, Any]):
  global texts, metadata
  embedding = model.encode([text])[0]  # This already returns a numpy array
  index.add(np.array([embedding], dtype='float32'))  # Wrap in array and specify dtype
  texts.append(text)
  metadata.append(meta)

def get_relevant_context(query: str, k: int = 5) -> List[Dict[str, Any]]:
  query_vector = model.encode([query])[0]
  D, I = index.search(np.array([query_vector], dtype='float32'), k)
  results = [{"text": texts[i], "metadata": metadata[i]} for i in I[0] if i < len(texts)]
  return results

def add_pdf_to_vector_store(pdf_text: str, pdf_name: str):
  chunks = chunk_text(pdf_text, chunk_size=1000, overlap=200)
  for i, chunk in enumerate(chunks):
      add_to_vector_store(chunk, {"source": pdf_name, "type": "pdf", "chunk": i})

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
  chunks = []
  start = 0
  while start < len(text):
      end = start + chunk_size
      chunk = text[start:end]
      chunks.append(chunk)
      start = end - overlap
  return chunks

def clear_vector_store():
  global index, texts, metadata
  index = faiss.IndexFlatL2(384)
  texts = []
  metadata = []

def get_all_content() -> str:
  return "\n\n".join([f"Source: {meta['source']}, Type: {meta['type']}\nContent: {text}" for text, meta in zip(texts, metadata)])

def remove_pdf_from_vector_store(pdf_name: str):
  global index, texts, metadata
  
  # Find indices of entries to remove
  indices_to_remove = [i for i, meta in enumerate(metadata) if meta['source'] == pdf_name and meta['type'] == 'pdf']
  
  if not indices_to_remove:
      return  # No entries found for this PDF
  
  # Remove entries from texts and metadata
  texts = [text for i, text in enumerate(texts) if i not in indices_to_remove]
  metadata = [meta for i, meta in enumerate(metadata) if i not in indices_to_remove]
  
  # Rebuild the index
  new_index = faiss.IndexFlatL2(384)  # 384 is the dimensionality of the chosen model
  for text in texts:
      embedding = model.encode([text])[0]
      new_index.add(np.array([embedding], dtype='float32'))
  
  # Replace the old index with the new one
  global index
  index = new_index

  print(f"Removed {len(indices_to_remove)} entries for PDF: {pdf_name}")