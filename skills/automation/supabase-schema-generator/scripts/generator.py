# generator.py
import os
import sys
import argparse
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """You are a Principal Database Administrator and SRE Architect.
Your task is to analyze the provided SQL schema definitions (DDL) and generate:
1. A clean TypeScript module containing type definitions/interfaces matching the tables.
2. A robust, production-grade SQL script defining Row Level Security (RLS) policies for Supabase.

CRITICAL REQUIREMENTS:
- Read the DDL carefully to identify primary keys, foreign keys, and relations.
- In the TypeScript file:
  - Export interface definitions for every table.
  - Correctly map SQL types to TypeScript types (e.g., VARCHAR/TEXT -> string, INT/DECIMAL -> number, BOOLEAN -> boolean, TIMESTAMP -> string, JSONB -> any).
- In the RLS SQL file:
  - Include statements to enable RLS: 'ALTER TABLE "table_name" ENABLE ROW LEVEL SECURITY;'
  - Create secure policies assuming standard multi-tenant setups where:
    - Users can only read, update, or delete their own data (based on auth.uid() matching a user_id or id column).
    - Authenticated users can insert data associated with their own auth.uid().
- Output formatting:
  - You must separate the TypeScript definitions and the RLS policies using these exact boundary markers:
    [TYPESCRIPT_TYPES]
    <Your generated TypeScript interfaces>
    [RLS_POLICIES]
    <Your generated Supabase RLS policies>
  - Do not wrap the outputs in markdown code block ticks.
"""

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        try:
            with open(r"C:\Users\araga\.hermes\.env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
    return api_key

def analyze_schema(client, ddl_content):
    prompt = f"Analyze this SQL schema and generate the TypeScript interfaces and Supabase RLS policies:\n\n{ddl_content}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.1
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Analyze SQL schemas to generate TS types and Supabase RLS policies.")
    parser.add_argument("-s", "--schema", required=True, help="Path to the input SQL schema file.")
    parser.add_argument("-t", "--output-types", default="types.ts", help="Target path to save TypeScript types.")
    parser.add_argument("-r", "--output-rls", default="policies.sql", help="Target path to save RLS policies.")

    args = parser.parse_args()

    if not os.path.exists(args.schema):
        print(f"Error: Schema file not found: {args.schema}", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not defined.", file=sys.stderr)
        sys.exit(1)

    with open(args.schema, "r", encoding="utf-8") as f:
        ddl_content = f.read()

    client = genai.Client(api_key=api_key)
    print(f"Analyzing schema file '{os.path.basename(args.schema)}' with Gemini...")
    
    raw_output = analyze_schema(client, ddl_content)

    # Parse boundaries
    ts_content = ""
    rls_content = ""

    if "[TYPESCRIPT_TYPES]" in raw_output and "[RLS_POLICIES]" in raw_output:
        parts = raw_output.split("[RLS_POLICIES]")
        ts_part = parts[0].replace("[TYPESCRIPT_TYPES]", "").strip()
        rls_part = parts[1].strip()
        
        # Clean any accidental code block markers
        ts_content = clean_code_blocks(ts_part)
        rls_content = clean_code_blocks(rls_part)
    else:
        # Fallback if boundaries are missing
        print("Warning: Gemini response missing structure boundaries. Saving raw output to both targets.", file=sys.stderr)
        ts_content = raw_output
        rls_content = raw_output

    # Write files
    with open(args.output_types, "w", encoding="utf-8") as f:
        f.write(ts_content + "\n")
    with open(args.output_rls, "w", encoding="utf-8") as f:
        f.write(rls_content + "\n")

    print(f"[SUCCESS] TypeScript types generated: {os.path.abspath(args.output_types)}")
    print(f"[SUCCESS] Supabase RLS policies generated: {os.path.abspath(args.output_rls)}")

def clean_code_blocks(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines.pop(0)
        if lines and lines[-1].startswith("```"):
            lines.pop(-1)
        text = "\n".join(lines).strip()
    return text

if __name__ == "__main__":
    main()
