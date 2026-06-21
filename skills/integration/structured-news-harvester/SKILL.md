# 🌐 Skill: structured-news-harvester

A lightweight, automated agent skill to harvest, clean, and summarize trending tech news from Hacker News using the Gemini API. Designed to bypass marketing clutter and generate natural, SRE-grade summary reports.

---

## 🛠️ Triggers

This skill is triggered when an agent or developer needs to gather the latest technical news, summarize discussions, or build a curated newsletter digest.
- "collect tech news"
- "summarize hacker news"
- "generate technical digest"
- "run structured-news-harvester"

---

## 🚀 Usage Guide

### Requirements
- Node.js (v18+)
- A valid `GEMINI_API_KEY` defined in the environment.

### Command Execution
Run the script using `node` from the repository root:

```bash
# Get top 5 stories and output to the default 'news_summary.md'
node skills/integration/structured-news-harvester/scripts/harvester.js

# Custom limit and custom output file path
node skills/integration/structured-news-harvester/scripts/harvester.js --limit 10 --output docs/weekly_digest.md
```

### Options
*   `-l`, `--limit`: Number of top stories to retrieve and summarize (default: `5`).
*   `-o`, `--output`: Target path to save the generated markdown file (default: `news_summary.md`).

---

## ⚡ SRE-Grade Curation

*   **Anti-Slop Processing:** Every news item is processed by Gemini under strict anti-slop guidelines. Clichés like "in today's digital landscape," "delve," or corporate marketing filler are automatically stripped.
*   **Network Resiliency:** Implements silent failover and warnings for single story network timeouts to ensure the script doesn't crash during network spikes.
