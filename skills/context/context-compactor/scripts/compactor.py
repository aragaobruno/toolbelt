# compactor.py
import os
import sys
import argparse
import ast
import re

def parse_python_file(file_path):
    """Parses a Python file using AST and extracts structure."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        return f"# Error parsing Python file {os.path.basename(file_path)}: {e}"
        
    lines = []
    
    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.indent = 0
            
        def visit_ClassDef(self, node):
            indent_str = "    " * self.indent
            lines.append(f"{indent_str}class {node.name}:")
            docstring = ast.get_docstring(node)
            if docstring:
                lines.append(f'{indent_str}    """{docstring}"""')
            
            self.indent += 1
            self.generic_visit(node)
            self.indent -= 1
            lines.append("")
            
        def visit_FunctionDef(self, node):
            indent_str = "    " * self.indent
            args = [arg.arg for arg in node.args.args]
            args_str = ", ".join(args)
            lines.append(f"{indent_str}def {node.name}({args_str}):")
            
            docstring = ast.get_docstring(node)
            if docstring:
                lines.append(f'{indent_str}    """{docstring}"""')
            lines.append(f"{indent_str}    ...")
            
        def visit_AsyncFunctionDef(self, node):
            indent_str = "    " * self.indent
            args = [arg.arg for arg in node.args.args]
            args_str = ", ".join(args)
            lines.append(f"{indent_str}async def {node.name}({args_str}):")
            
            docstring = ast.get_docstring(node)
            if docstring:
                lines.append(f'{indent_str}    """{docstring}"""')
            lines.append(f"{indent_str}    ...")

    v = Visitor()
    v.visit(tree)
    return "\n".join(lines)

def parse_js_ts_file(file_path):
    """Parses a JS/TS file using regex and extracts structure."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return f"# Error reading JS/TS file {os.path.basename(file_path)}: {e}"
    
    output = []
    in_docblock = False
    current_docblock = []
    
    for line in lines:
        line_strip = line.strip()
        
        # Capture JSDoc comments
        if line_strip.startswith("/**"):
            in_docblock = True
            current_docblock = [line_strip]
            continue
        elif in_docblock:
            current_docblock.append(line_strip)
            if line_strip.endswith("*/"):
                in_docblock = False
            continue
            
        # Class definition
        class_match = re.match(r'^(export\s+)?(default\s+)?class\s+(\w+)', line_strip)
        if class_match:
            class_name = class_match.group(3)
            if current_docblock:
                output.extend(current_docblock)
                current_docblock = []
            output.append(f"class {class_name} {{")
            continue
            
        # Function/Method definition
        func_match = re.match(r'^(async\s+)?(export\s+)?(default\s+)?function\s+(\w+)\s*\(', line_strip)
        method_match = re.match(r'^(async\s+)?(public|private|protected\s+)?(\w+)\s*\(', line_strip)
        
        if func_match:
            func_name = func_match.group(4)
            if current_docblock:
                output.extend(current_docblock)
                current_docblock = []
            output.append(f"function {func_name}() {{ ... }}")
        elif method_match:
            method_name = method_match.group(3)
            if method_name not in ['if', 'for', 'while', 'switch', 'catch']:
                if current_docblock:
                    output.extend(current_docblock)
                    current_docblock = []
                output.append(f"  {method_name}() {{ ... }}")
                
        if not line_strip:
            current_docblock = []
            
    return "\n".join(output)

def compact_directory(directory, exclude_patterns):
    summary_parts = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'dist', 'build']]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            
            should_exclude = False
            for pat in exclude_patterns:
                if pat and (pat in rel_path or pat in file):
                    should_exclude = True
                    break
            if should_exclude:
                continue
                
            ext = os.path.splitext(file)[1]
            if ext == '.py':
                summary_parts.append(f"File: {rel_path} (Python)\n" + "=" * 40)
                summary_parts.append(parse_python_file(file_path))
                summary_parts.append("\n")
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                summary_parts.append(f"File: {rel_path} (JavaScript/TypeScript)\n" + "=" * 40)
                summary_parts.append(parse_js_ts_file(file_path))
                summary_parts.append("\n")
                
    return "\n".join(summary_parts)

def main():
    parser = argparse.ArgumentParser(description="Compacts codebase directories for token optimization.")
    parser.add_argument("directory", help="Root directory to compact")
    parser.add_argument("--output", required=True, help="Path to the output summary file")
    parser.add_argument("--exclude", default="", help="Comma-separated exclude patterns (e.g. test,build)")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory does not exist: {args.directory}", file=sys.stderr)
        sys.exit(1)
        
    exclude_patterns = [p.strip() for p in args.exclude.split(",")]
    
    print(f"Scanning directory: {args.directory}...")
    compact_text = compact_directory(args.directory, exclude_patterns)
    
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(compact_text)
        print(f"\n[SUCCESS] Compaction completed!")
        print(f"Summary saved at: {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
