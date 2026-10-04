# Local Agentic File Organizer & Memory Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Local-First](https://img.shields.io/badge/architecture-local%2ofirst-green.svg)](https://ollama.com/)

A production-grade, modular, privacy-first local AI agent built in Python that monitors workspace directories, detects normalized file deltas, generates chronological immutable audit reports, and performs local semantic vector search over historical logs using **Ollama**, **SQLite**, and **NumPy**—completely offline with zero cloud dependency or recurring subscription fees.

---

## 🌟 Why This Agent Stands Out

Traditional file organizers rely on rigid, brittle rule engines (like extension matching or static regex) that break on edge cases, while consumer AI sorters lock you into expensive, black-box cloud subscriptions that compromise data privacy. 

This engine is engineered for professionals and developers who demand absolute control:
- **100% Local & Air-Gapped:** Runs entirely on your hardware using local models (`qwen3.5:latest`, `nomic-embed-text:latest`) via Ollama, ensuring sensitive documents never leave your machine.
- **Zero Redundancy (Delta Engine):** Leverages an indexed SQLite ledger and OS-normalized file signatures (`mtime` + size) to process *only* newly added or modified files.
- **Long-Term Cognitive Memory:** Combines SQLite state tracking and local vector embeddings so the agent can semantically search past execution logs for historical context.
- **Immutable Audit Trails:** Never overwrites past work. Every execution drops a timestamped chronological report into an isolated history ledger.
- **Strictly Modular Architecture:** Separates configuration, database repositories, provider clients, and extensible tool registries for effortless scaling.

---

## 📁 Project Structure

```text
organiser-agent/
│
├── .env.example          # Environment variable template
├── .gitignore            # Git exclusion rules
├── LICENSE.txt           # MIT Open Source License
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contribution guidelines & developer standards
├── requirements.txt      # Python dependencies
├── prompts.json          # Tunable system instructions and user templates
├── main.py               # Application entry point & agent execution loop
│
├── core/
│   ├── __init__.py
│   ├── config.py         # Environment configuration loader
│   ├── database.py       # SQLite connection & state checkpointing repo
│   └── llm.py            # Unified LLM & embedding client factory
│
├── tools/
│   ├── __init__.py
│   ├── file_ops.py       # Workspace file reader & immutable audit logging tools
│   ├── memory.py         # Vector semantic search over historical run reports
│   └── registry.py       # Centralized tool schemas & function mapping
│
├── history/              # Generated immutable run reports (Auto-created)
└── test_workspace/       # Monitored workspace directory (Auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.10+** installed along with a running local instance of **[Ollama](https://ollama.com/)**. Pull the required local LLM and embedding models:

```bash
ollama pull qwen3.5:latest
ollama pull nomic-embed-text:latest
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/organiser-agent.git
   cd organiser-agent
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

---

## ⚙️ Configuration

### 1. Environment Settings (`.env`)

Customize runtime parameters, model choices, API endpoints, and directory paths in `.env`:

```env
PROVIDER=ollama
LLM_MODEL=qwen3.5:latest
EMBEDDING_MODEL=nomic-embed-text:latest
OLLAMA_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=your_openai_api_key_here
DB_PATH=agent_state.db
WORKSPACE_DIR=./test_workspace
HISTORY_DIR=./history
```

### 2. Tuning Prompts (`prompts.json`)

Modify agent personas, system prompts, and prompt templates dynamically without touching Python application code:

```json
{
  "system_prompt": "You are a professional local file organizer agent with long-term memory. Use search_historical_reports if you need context from past runs.",
  "user_prompt_template": "New delta files detected: {delta_files_json}. You have access to historical memory search. If needed, search past reports using search_historical_reports, analyze the new files, and store a chronological summary using write_immutable_summary."
}
```

---

## 💡 Usage Workflow

1. **Add Workspace Files:**
   Place or create files you want the agent to analyze inside `test_workspace/`.

2. **Run the Agent:**
   Execute the main entry script:
   ```bash
   python main.py
   ```

3. **Execution & Audit:**
   - The delta engine scans `test_workspace/` for new or modified items.
   - The agent analyzes file content, searches past memory for historical context, and writes an immutable report in `history/`.
   - The engine checkpoints state in `agent_state.db` to avoid re-processing unmodified files on subsequent runs.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code style, modular architecture guidelines, and the pull request process.

---

## 📄 License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more information.
