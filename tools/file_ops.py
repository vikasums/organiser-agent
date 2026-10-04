from datetime import datetime
import json
import os
from core.config import HISTORY_DIR, WORKSPACE_DIR
from core.database import get_connection


def is_safe_path(base_dir: str, target_path: str) -> bool:
  abs_base = os.path.abspath(base_dir)
  abs_target = os.path.abspath(target_path)
  try:
    return os.path.commonpath([abs_base, abs_target]) == abs_base
  except ValueError:
    return False


def read_text_file(file_name: str) -> str:
  abs_target = os.path.join(WORKSPACE_DIR, file_name)
  if not is_safe_path(WORKSPACE_DIR, abs_target):
    return (
        f"Security Error: Access denied to '{file_name}'. Path traversal"
        " outside WORKSPACE_DIR is prohibited."
    )

  try:
    with open(abs_target, "r", encoding="utf-8") as f:
      return f.read()
  except Exception as e:
    return f"Error reading file: {str(e)}"


def write_immutable_summary(content: str) -> str:
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  summary_filename = f"run_report_{timestamp}.txt"
  summary_path = os.path.join(HISTORY_DIR, summary_filename)

  with open(summary_path, "w", encoding="utf-8") as f:
    f.write(content)

  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO run_history (summary_path, files_processed) VALUES (?, ?)",
      (summary_path, 1),
  )
  conn.commit()
  conn.close()

  return f"Successfully committed immutable audit report to {summary_path}"
