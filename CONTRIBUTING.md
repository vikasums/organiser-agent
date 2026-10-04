# Contributing to Local Agentic File Organizer

Thank you for your interest in contributing! 🎉 All contributions—bug reports, feature requests, documentation updates, and pull requests—are highly appreciated.

## 🛠️ How to Contribute

### 1. Reporting Bugs
When opening an issue for a bug, please include:
- Your operating system and Python version (`python --version`).
- Step-by-step instructions to reproduce the issue.
- Relevant traceback logs or error outputs.

### 2. Suggesting Features
If you have an idea for a new capability (such as a new tool or integration), please open an issue to discuss the use case and architectural approach before submitting code.

### 3. Submitting Pull Requests
1. Fork the repository and clone your fork locally:
   ```bash
   git clone https://github.com/your-username/organiser-agent.git
   cd organiser-agent
   ```
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Implement your changes adhering to the project's modular design pattern (`core/` for infrastructure, `tools/` for capabilities).
4. Verify that imports resolve cleanly and state management remains crash-resilient.
5. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add custom file filter to delta scanning engine"
   ```
6. Push to your branch and open a Pull Request against `main`.

---

## 📐 Code Style & Architecture Guidelines

- **Separation of Concerns:** Keep core application logic out of `main.py`. Database queries belong in `core/database.py`, configuration in `core/config.py`, LLM & Embedding provider clients in `core/llm.py`, and tool definitions in `tools/`.
- **Environment Parity:** Never hardcode paths, API keys, endpoints, or model names. Always utilize `core/config.py` and environment variables.
- **Modularity:** Ensure new features expose clean function signatures and tool schemas registered in `tools/registry.py`.
- **Robust State Management:** Ensure file operations handle exceptions gracefully and state checkpoints in `agent_state.db` remain crash-resilient.
