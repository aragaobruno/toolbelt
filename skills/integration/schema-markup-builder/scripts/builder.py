# builder.py
import os
import sys
import argparse
import json
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """You are a Search Engine Optimization (SEO) Architect specializing in technical SEO and semantic markup.
Your task is to generate a highly optimized, fully compliant JSON-LD schema based on the provided business information.

CRITICAL REQUIREMENTS:
1. Output ONLY the raw JSON-LD structure inside a valid JSON object.
2. Do not wrap the output in HTML <script> tags.
3. Do not include markdown code block formatting (e.g., do not wrap in ```json or ```).
4. Strictly follow the schema.org specifications.
5. If the type is 'LocalBusiness' or one of its subtypes (like 'HairSalon', 'AutomotiveBusiness', 'LegalService'), include:
   - '@context': 'https://schema.org'
   - '@type': the specific subtype
   - 'name'
   - 'url'
   - 'address' (PostalAddress structure: streetAddress, addressLocality, addressRegion, postalCode, addressCountry)
   - 'telephone'
   - 'image'
   - 'priceRange' (if not specified, use '$$')
6. Ensure all keys and values are correctly formatted and there are no trailing commas that violate standard JSON syntax.
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

def generate_schema(client, biz_info, schema_type):
    prompt = f"Generate a JSON-LD schema of type '{schema_type}' using the following details:\n\n{json.dumps(biz_info, indent=2, ensure_ascii=False)}"
    
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
    parser = argparse.ArgumentParser(description="Generate valid JSON-LD SEO Schema markup using Gemini.")
    parser.add_argument("-b", "--business", required=True, help="Name of the business.")
    parser.add_argument("-u", "--url", required=True, help="URL of the business website.")
    parser.add_argument("-t", "--type", default="LocalBusiness", help="Schema type (e.g., LocalBusiness, Organization, Product).")
    parser.add_argument("-o", "--output", default="schema.json", help="Path to save the generated JSON-LD schema.")
    parser.add_argument("-p", "--params", help="Path to a JSON file containing additional parameters (address, phone, hours, etc.) or raw JSON string.")

    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not defined.", file=sys.stderr)
        sys.exit(1)

    # Base parameters
    biz_info = {
        "name": args.business,
        "url": args.url
    }

    # Load additional parameters if provided
    if args.params:
        if os.path.exists(args.params):
            try:
                with open(args.params, "r", encoding="utf-8") as f:
                    extra_params = json.load(f)
                    biz_info.update(extra_params)
            except Exception as e:
                print(f"Warning: Failed to load parameters from file: {e}", file=sys.stderr)
        else:
            try:
                extra_params = json.loads(args.params)
                biz_info.update(extra_params)
            except Exception as e:
                print(f"Warning: Could not parse parameters string as JSON: {e}", file=sys.stderr)

    client = genai.Client(api_key=api_key)
    print(f"Generating '{args.type}' schema for: {args.business}...")
    
    schema_text = generate_schema(client, biz_info, args.type)
    
    # Clean output
    schema_text = schema_text.strip()
    if schema_text.startswith("```"):
        lines = schema_text.split("\n")
        if lines[0].startswith("```"):
            lines.pop(0)
        if lines and lines[-1].startswith("```"):
            lines.pop(-1)
        schema_text = "\n".join(lines).strip()

    # Validate JSON syntax
    try:
        json_obj = json.loads(schema_text)
        # Ensure it has @context and @type
        if "@context" not in json_obj:
            json_obj["@context"] = "https://schema.org"
        if "@type" not in json_obj:
            json_obj["@type"] = args.type
        schema_text = json.dumps(json_obj, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Gemini output is not strictly valid JSON: {e}. Saving raw text anyway.", file=sys.stderr)

    output_path = os.path.abspath(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(schema_text + "\n")
        
    print(f"[SUCCESS] Schema markup generated and saved successfully to: {output_path}")

if __name__ == "__main__":
    main()
