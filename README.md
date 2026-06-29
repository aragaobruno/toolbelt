# 🛠️ toolbelt

A curated collection of modular, production-ready **AI Agent Skills** and utility scripts designed to supercharge autonomous developer workflows. Built with an SRE (Site Reliability Engineering) and Unix-like philosophy: highly cohesive, loosely coupled, and token-efficient.

This repository serves as a portfolio demonstrating advanced concepts in **AI Engineering**, context optimization, secure automation, and robust error-handling.

---

## 🗂️ Registry of Skills

Here are the developed skills structured logically and sequentially:

### 🧠 Category: Context Engineering & Quality (Phase 1)
*   **[`ai-slop-detector`](skills/context/ai-slop-detector):** Prose and code auditor. Detects generic AI-generated jargon ("AI-slop") and sanitizes output files to make them sound human, natural, and direct.
*   **[`context-compactor`](skills/context/context-compactor):** Source code compactor. Scans large file trees and generates lightweight structural maps containing only classes, methods, signatures, and docstrings for token context window optimization.

### 🛠️ Category: DevOps & Git Workflows (Phase 2)
*   **[`smart-pr-generator`](skills/devops/smart-pr-generator):** Conventional Commit and SRE-grade Pull Request description generator from Git diffs. Includes built-in AI-slop filtering and options for interactive commit creation.
*   **[`unit-test-bootstrapper`](skills/devops/unit-test-bootstrapper):** Automated unit test suite generator (pytest for Python, Jest for JS/TS). Analyzes source code files using Gemini to bootstrap comprehensive test suites covering happy paths, edge cases, and error handling.
*   **[`local-vram-orchestrator`](skills/devops/local-vram-orchestrator):** Local model VRAM optimizer. Manages GPU memory limits (6GB VRAM) for sequential execution (LLMs, TTS, SD, CLIP), enforcing file-lock serialization and dynamic CUDA cache flushes.

### 🌐 Category: Data Integration & APIs (Phase 3)
*   **[`structured-news-harvester`](skills/integration/structured-news-harvester):** Real-time technical news and discussion scraper (Hacker News). Uses Gemini to filter noise, clickbait, and marketing fluff, producing clean executive summaries in Markdown.
*   **[`schema-markup-builder`](skills/integration/schema-markup-builder):** Automated generator for Google-compliant SEO structured data (JSON-LD). Streamlines creation of schema.org markups for local businesses, organization portfolios, and products.
*   **[`cyber-fraud-forensics`](skills/integration/cyber-fraud-forensics):** Digital brand protection and phishing forensics. Defines SOPs for network evidence capture and generates structured forensic Abuse Reports for hosting/registrar notification.

### 🗄️ Category: Database & Workflow Automation (Phase 4)
*   **[`supabase-schema-generator`](skills/automation/supabase-schema-generator):** SRE-grade database schema interpreter (Python). Automatically reverse-engineers SQL DDL files to output clean frontend TypeScript type interfaces and secure Supabase Row Level Security (RLS) policies.
*   **[`n8n-workflow-packer`](skills/automation/n8n-workflow-packer):** DevSecOps sanitization utility for n8n workflows (Node.js). Strips and redacts API tokens, private credential IDs, and active webhook URLs from workflow JSON files to allow secure version control.

---

## 🚀 How It Works

Each skill in this collection is packaged in its own directory under `skills/` following the Google Antigravity standard structure:

```text
skills/[category]/[skill-name]/
├── SKILL.md        # Behavior declarations, triggers, and metadata
└── scripts/        # CLI scripts (Python with uv, or Node.js)
```

### Adopted Engineering Principles:
1.  **Token Efficiency:** LLM context windows are expensive. Our tools minimize the volume of raw code and text sent to agents.
2.  **Declarative Rate Limiting:** All API integrations enforce exponential backoff and structured handling of HTTP 429 status codes.
3.  **Prose Cleanliness:** Output files are audited to ensure direct, human-written style, free of AI conversational clutter.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
