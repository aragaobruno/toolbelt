# 🌐 Skill: schema-markup-builder

An automated utility skill to build valid, highly optimized schema.org JSON-LD structured data for technical SEO. Excellent for optimizing Local Business visibility, organizational SEO, and product schema.

---

## 🛠️ Triggers

This skill is triggered when an agent or developer needs to generate structured JSON-LD schemas, build SEO markups, or prepare rich snippet scripts for websites.
- "generate seo schema"
- "build json-ld schema"
- "run schema-markup-builder"
- "create localbusiness schema"

---

## 🚀 Usage Guide

### Requirements
- Python (3.10+)
- `google-genai` package installed (via `uv`)
- A valid `GEMINI_API_KEY` defined in the environment or in the global `.hermes/.env` file.

### Command Execution
Run the script using `uv run` from the repository root:

```bash
# Basic LocalBusiness schema
uv run --with google-genai skills/integration/schema-markup-builder/scripts/builder.py \
  --business "Bruno's Coffee Shop" \
  --url "https://brunoscoffeeshop.com"

# Custom Schema Type with extra parameters
uv run --with google-genai skills/integration/schema-markup-builder/scripts/builder.py \
  --business "Bruno's Coffee Shop" \
  --url "https://brunoscoffeeshop.com" \
  --type "Cafe" \
  --params '{"telephone": "+1 212-555-0199", "address": {"streetAddress": "123 Main Street", "addressLocality": "New York", "addressRegion": "NY", "postalCode": "10001", "addressCountry": "US"}}' \
  --output "docs/cafe_schema.json"
```

### Options
*   `-b`, `--business`: Name of the business (required).
*   `-u`, `--url`: Main website URL (required).
*   `-t`, `--type`: Schema.org type, e.g., `LocalBusiness`, `HairSalon`, `Organization`, `Product` (default: `LocalBusiness`).
*   `-p`, `--params`: Path to a JSON file or a raw JSON string containing extra parameters.
*   `-o`, `--output`: Target path to save the generated JSON file (default: `schema.json`).
