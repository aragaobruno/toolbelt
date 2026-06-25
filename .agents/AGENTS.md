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
*   **Primary Tool:** For any task involving web scraping, data extraction from HTML/XML/JSON/Markdown, or gathering unstructured online data, **always prioritize ScrapeGraphAI**.
*   **Self-Healing Pipelines:** Leverage LLM-driven graph extraction (e.g. `SmartScraperGraph`, `SearchGraph`) instead of writing brittle manual selectors.
*   **Local Execution SRE Rules:** Integrate ScrapeGraphAI locally, utilizing Ollama for local LLM inference when possible to optimize costs, while preserving credential security boundaries.

