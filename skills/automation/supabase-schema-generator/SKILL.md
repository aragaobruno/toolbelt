# 🗄️ Skill: supabase-schema-generator

An SRE-grade automation skill to parse SQL schemas and auto-generate safe TypeScript interfaces for the frontend and Row Level Security (RLS) policies for Supabase.

---

## 🛠️ Triggers

This skill is triggered when an agent or developer needs to translate database tables into frontend types, secure Supabase tables, or generate RLS scripts.
- "generate supabase rls"
- "build typescript database types"
- "run supabase-schema-generator"
- "create db types"

---

## 🚀 Usage Guide

### Requirements
- Python (3.10+)
- `google-genai` package installed (via `uv`)
- A valid `GEMINI_API_KEY` defined in the environment or in the global `.hermes/.env` file.

### Command Execution
Run the script using `uv run` from the repository root:

```bash
# Generate types and RLS policies from schema.sql
uv run --with google-genai skills/automation/supabase-schema-generator/scripts/generator.py \
  --schema database_schema.sql \
  --output-types src/types/database.ts \
  --output-rls supabase/migrations/policies.sql
```

### Options
*   `-s`, `--schema`: Path to the input SQL schema file (required).
*   `-t`, `--output-types`: Path to save the generated TypeScript types (default: `types.ts`).
*   `-r`, `--output-rls`: Path to save the generated RLS SQL script (default: `policies.sql`).
