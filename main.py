import json
import os
import sqlite3
from core.config import LLM_MODEL, PROVIDER, WORKSPACE_DIR
from core.database import get_connection, init_db
from core.llm import get_llm_client
from tools.registry import AVAILABLE_TOOLS, TOOLS_SCHEMA


def get_delta_files(target_dir: str):
  init_db()
  conn = get_connection()
  cursor = conn.cursor()

  delta_files = []
  abs_target = os.path.abspath(target_dir)

  for root, _, files in os.walk(abs_target):
    for file in files:
      if file.startswith("."):
        continue

      full_path = os.path.join(root, file)
      rel_path = os.path.normpath(os.path.relpath(full_path, abs_target))

      try:
        stat = os.stat(full_path)
        size = stat.st_size
        mtime = round(stat.st_mtime, 2)

        cursor.execute(
            """
                SELECT status FROM processed_files 
                WHERE file_path = ? AND file_size = ? AND mtime = ?
            """,
            (rel_path, size, mtime),
        )
        if not cursor.fetchone():
          delta_files.append({"path": rel_path, "size": size, "mtime": mtime})
      except Exception:
        continue

  conn.close()
  return delta_files


def run_super_organizer():
  init_db()
  print(f"[Engine Active] Provider: {PROVIDER.upper()} | Model: {LLM_MODEL}")

  delta_files = get_delta_files(WORKSPACE_DIR)
  if not delta_files:
    print("[Delta Engine] No changes detected. Workspace is fully synchronized.")
    return

  print(f"[Delta Engine] Found {len(delta_files)} new/modified item(s).")

  client = get_llm_client()
  
  system_prompt = (
      "You are a professional local file organizer agent with long-term"
      " memory. Use search_historical_reports if you need context from"
      " past runs."
  )
  user_prompt_template = (
      "New delta files detected: {delta_files_json}. You have access to"
      " historical memory search. If needed, search past reports using"
      " search_historical_reports, analyze the new files, and store a"
      " chronological summary using write_immutable_summary."
  )

  prompts_path = os.path.join(os.path.dirname(__file__), "prompts.json")
  if os.path.exists(prompts_path):
    try:
      with open(prompts_path, "r", encoding="utf-8") as f:
        prompts_cfg = json.load(f)
        system_prompt = prompts_cfg.get("system_prompt", system_prompt)
        user_prompt_template = prompts_cfg.get(
            "user_prompt_template", user_prompt_template
        )
    except Exception as e:
      print(f"[Warning] Failed to load prompts.json: {e}")

  user_prompt = user_prompt_template.format(
      delta_files_json=json.dumps(delta_files)
  )

  messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_prompt},
  ]

  for turn in range(6):
    response = client.chat.completions.create(
        model=LLM_MODEL, messages=messages, tools=TOOLS_SCHEMA
    )

    msg = response.choices[0].message
    messages.append(msg)

    if msg.tool_calls:
      for call in msg.tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments)
        print(f"  -> Executing Tool: {name} with {args}")

        output = (
            AVAILABLE_TOOLS[name](**args)
            if name in AVAILABLE_TOOLS
            else "Tool not found."
        )
        print(f"  <- Output: {output[:150]}...")

        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": str(output),
        })
    else:
      print("\nAgent Final Answer:")
      print(msg.content)

      # Checkpoint state to SQLite
      conn = get_connection()
      cursor = conn.cursor()
      for f in delta_files:
        cursor.execute(
            """
                INSERT OR REPLACE INTO processed_files (file_path, file_size, mtime, status)
                VALUES (?, ?, ?, 'completed')
            """,
            (f["path"], f["size"], f["mtime"]),
        )
      conn.commit()
      conn.close()
      print("[State Secured] All files safely committed to SQLite ledger.")
      break


if __name__ == "__main__":
  run_super_organizer()
