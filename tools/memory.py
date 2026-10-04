import os
import sqlite3
from core.config import EMBEDDING_MODEL
from core.database import get_connection
from core.llm import get_embedding_client
import numpy as np


def search_historical_reports(query_string: str) -> str:
  embed_client = get_embedding_client()
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT summary_path, timestamp FROM run_history")
  rows = cursor.fetchall()
  conn.close()

  if not rows:
    return "No historical run reports found in memory yet."

  try:
    query_resp = embed_client.embeddings.create(
        model=EMBEDDING_MODEL, input=query_string
    )
    query_vector = np.array(query_resp.data[0].embedding)
  except Exception as e:
    return f"Error generating search vector: {str(e)}"

  results = []
  for summary_path, timestamp in rows:
    if not os.path.exists(summary_path):
      continue
    try:
      with open(summary_path, "r", encoding="utf-8") as f:
        content = f.read()

      chunk_resp = embed_client.embeddings.create(
          model=EMBEDDING_MODEL, input=content[:2000]
      )
      content_vector = np.array(chunk_resp.data[0].embedding)

      similarity = np.dot(query_vector, content_vector) / (
          np.linalg.norm(query_vector) * np.linalg.norm(content_vector)
      )
      results.append((float(similarity), timestamp, summary_path, content))
    except Exception:
      continue

  if not results:
    return "No relevant historical matches found."

  results.sort(key=lambda x: x[0], reverse=True)
  best = results[0]

  return (
      f"Found Historical Match (Similarity Score: {best[0]:.4f} at"
      f" {best[1]}):\nFile: {best[2]}\nSnippet:\n{best[3][:800]}"
  )
