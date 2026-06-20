# bootstrapper.py
import os
import sys
import argparse
from google import genai
from google.genai import types

# System Instruction for Gemini
SYSTEM_INSTRUCTION = """You are a Principal Software Engineer specializing in Quality Assurance and Test-Driven Development (TDD).
Your task is to analyze the provided source code file and generate a robust, production-grade unit test suite.

CRITICAL REQUIREMENTS:
1. Detect the programming language of the provided source code (usually Python, JavaScript, or TypeScript).
2. If Python: Generate tests using 'pytest'. Use standard pytest assert syntax.
3. If JavaScript/TypeScript: Generate tests using 'Jest' (ESM or CommonJS style depending on syntax).
4. Cover:
   - Happy paths (standard correct inputs and expected outputs).
   - Edge cases (null/undefined, empty strings/lists, out of bounds).
   - Error handling (verifying that the code throws exceptions or returns error structures).
5. Mock external API calls, HTTP requests, or database queries where appropriate.
6. Output ONLY the code of the test file. Do not include markdown code block formatting (e.g., do not wrap in ```python or ```javascript). Return raw code."""

def get_api_key():
    # Try GEMINI_API_KEY first, fallback to GOOGLE_API_KEY
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # Fallback check for active hermes configuration env
        try:
            with open(r"C:\Users\araga\.hermes\.env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
            
    return api_key

def generate_unit_tests(source_code, filename, api_key):
    client = genai.Client(api_key=api_key)
    
    prompt = f"Analyze this source code from file '{filename}' and generate a comprehensive unit test file:\n\n{source_code}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Auto-generate unit tests from source files using Gemini.")
    parser.add_argument("file", help="Path to the source code file to generate tests for.")
    parser.add_argument("-o", "--output", help="Path to save the generated test file (default: test_<file_basename>).")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
        
    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not defined.", file=sys.stderr)
        sys.exit(1)
        
    with open(args.file, "r", encoding="utf-8") as f:
        source_code = f.read()
        
    basename = os.path.basename(args.file)
    print(f"Analyzing {basename} and generating unit tests with Gemini...")
    
    test_code = generate_unit_tests(source_code, basename, api_key)
    
    # Strip any potential markdown wrappers if returned by the model
    if test_code.startswith("```"):
        lines = test_code.split("\n")
        # Remove first and last line
        if lines[0].startswith("```"):
            lines.pop(0)
        if lines and lines[-1].startswith("```"):
            lines.pop(-1)
        test_code = "\n".join(lines)
        
    # Determine default output filename
    output_path = args.output
    if not output_path:
        dir_name = os.path.dirname(args.file)
        name, ext = os.path.splitext(basename)
        if ext in ['.py']:
            output_path = os.path.join(dir_name, f"test_{name}{ext}")
        elif ext in ['.js', '.ts', '.tsx', '.jsx']:
            output_path = os.path.join(dir_name, f"{name}.test{ext}")
        else:
            output_path = os.path.join(dir_name, f"{name}_test{ext}")
            
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(test_code.strip() + "\n")
        
    print(f"✅ Unit tests generated and saved successfully to: {output_path}")

if __name__ == "__main__":
    main()
