# Workspace Rules & Memory: Bruno Aragão Vivan

These rules define the project-level engineering guidelines, architectural preferences, and positioning strategies for Bruno Aragão Vivan.

---

## 🎯 1. Professional Positioning: The AI Product Builder
*   **Orchestrator Role:** Treat Bruno as a **Technical Product Leader & AI Systems Orchestrator**. Focus on conceptual design, architectural interfaces, business rules, and API flows.
*   **AI-Assisted Workflow:** Acknowledge that the core development workflow leverages **Google AntiGravity + Claude** as the execution engines, while Bruno defines scope, priorities, and acceptance criteria.

---

## 🤖 2. Multi-Agent Orchestration: CrewAI Framework
*   **Primary Framework:** For any system requiring multiple cooperating agents, asynchronous execution, task delegation, or complex sequential workflows, **always prioritize and recommend CrewAI**.
*   **Local Execution SRE Rules:** Ensure CrewAI runs locally in the Python workspace, integrating with local databases (PostgreSQL/Supabase) and keeping strict credentials security boundaries.
*   **Lightweight UI:** Recommend coupling local CrewAI projects with **Streamlit** or **Chainlit** interfaces to provide Bruno with a visual dashboard to interact with his crews.

---

## 🕷️ 3. Intelligent Web Scraping: ScrapeGraphAI
*   **Self-Healing Pipelines:** Leverage LLM-driven graph extraction (e.g. `SmartScraperGraph`, `SearchGraph`) instead of writing brittle manual selectors.
*   **Local Execution SRE Rules:** Integrate ScrapeGraphAI locally, utilizing Ollama for local LLM inference when possible to optimize costs, while preserving credential security boundaries.

---

## 🔌 4. Model Context Protocol (MCP) Servers
*   **Active Servers:** The following MCP servers are globally configured in `C:\Users\araga\.gemini\antigravity\mcp_config.json` and available for use in our workflows:
    *   `perplexity`: Live web search and deep research (requires API key).
    *   `playwright`: Dynamic browser automation, UI testing, and screenshots.
    *   `firecrawl`: Clean markdown crawler for scraping large sites efficiently (requires API key).
    *   `glyph`: Multimedia vision computer and visual verification tools.
    *   `chrome-devtools`: Connects directly to Bruno's active Chrome browser via remote debugging (`--remote-debugging-port=9222`).
    *   `github`: Repository manipulation, pull requests, and automation.
    *   `git`: Local git repository reading, commit logs, and branch management.
    *   `docker`: Local Docker container management (inspecting, starting, stopping services).
    *   `slack`: Posting alerts and reading messages in channels (requires bot token).
    *   `postgres-toolbox` & `mysql-toolbox`: Structured database inspection and query tools.

---

## 📚 5. Local Orchestration & Reference Libraries
*   **Architectural References:** The following codebases are cloned locally in `C:\Users\araga\.gemini\antigravity\scratch/` for direct architectural reference, implementation examples, and design patterns:
    *   `crewai/`: Multi-agent orchestration and task delegation.
    *   `scrapegraph-ai/`: AI-driven graph web scraping with Pydantic output.
    *   `langgraph/`: Stateful, cyclical graph-based multi-agent workflows.
    *   `agno/`: Lightweight memory, tool, and vector DB connectors for LLMs.
    *   `PraisonAI/`: Declarative YAML-based multi-agent configurations.
    *   `open-webui/`: Private, self-hosted web UI for local/cloud LLMs.
---

## 🛠️ 6. SRE Architectural Guidelines
When designing or building software systems (such as Aegis Nexus, ai-video-factory, or toolbelt), always adhere to these performance and security guidelines:
*   **Security (Zero Hardcoding):** Never hardcode secrets or API tokens. Reference them via environment variables (e.g. `$VAR`) in MCP configs and load them from `.env` or system environment context in code.
*   **API Cost Optimization (Pre-filtering):** Before feeding raw online data (like CertStream feeds or large web-crawls) to expensive multimodal LLM APIs, implement a fast, local pre-filter (e.g. Levenshtein distance, regex, or local small models).
*   **Memory Efficiency (GPU VRAM Flush):** On local execution tasks utilizing GPUs (such as Stable Diffusion or Whisper pipelines on the 6GB RTX 4050), explicitly clear CUDA cache (`torch.cuda.empty_cache()` and `gc.collect()`) after each sequential step to prevent Out of Memory (OOM) errors.
*   **Human-in-the-loop (Slack/Mem0):** Link system alerts to Slack interactive buttons. Action logs (approvals/rejections) from humans must update the local Mem0 memory to continuously align agent behavior.
*   **Self-Healing Code Pipelines:** Integrate toolbelt automation to intercept system error logs, query documentation via Perplexity MCP, run local tests on db toolboxes, and autonomously open Git pull requests for code corrections.

