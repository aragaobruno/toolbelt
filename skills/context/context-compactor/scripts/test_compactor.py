import pytest
import os
import sys
import argparse
from unittest.mock import patch, mock_open, MagicMock

# Assuming the functions are in a file named 'compactor.py'
# We need to import them.
from compactor import (
    parse_python_file,
    parse_js_ts_file,
    compact_directory,
    main
)

# --- Tests for parse_python_file ---

def test_parse_python_file_simple(tmp_path):
    """Test parsing a simple Python file with a class and a function."""
    file_content = """
class MyClass:
    \"\"\"A simple class.\"\"\"
    def __init__(self, name):
        \"\"\"Constructor.\"\"\"
        pass

    def my_method(self):
        \"\"\"A method.\"\"\"
        pass

def my_function(arg1, arg2):
    \"\"\"A simple function.\"\"\"
    return arg1 + arg2
"""
    expected_output = """class MyClass:
    \"\"\"A simple class.\"\"\"
    def __init__(self, name):
        \"\"\"Constructor.\"\"\"
        ...
    def my_method(self):
        \"\"\"A method.\"\"\"
        ...

def my_function(arg1, arg2):
    \"\"\"A simple function.\"\"\"
    ..."""
    
    p = tmp_path / "test.py"
    p.write_text(file_content)
    
    result = parse_python_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_python_file_async(tmp_path):
    """Test parsing a Python file with async functions."""
    file_content = """
async def async_func(data):
    \"\"\"An async function.\"\"\"
    await some_call(data)

class AsyncHandler:
    async def handle(self, request):
        \"\"\"Handle async request.\"\"\"
        pass
"""
    expected_output = """async def async_func(data):
    \"\"\"An async function.\"\"\"
    ...
class AsyncHandler:
    async def handle(self, request):
        \"\"\"Handle async request.\"\"\"
        ..."""
    
    p = tmp_path / "async_test.py"
    p.write_text(file_content)
    
    result = parse_python_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_python_file_empty(tmp_path):
    """Test parsing an empty Python file."""
    p = tmp_path / "empty.py"
    p.write_text("")
    result = parse_python_file(str(p))
    assert result == ""

def test_parse_python_file_comments_only(tmp_path):
    """Test parsing a Python file with only comments and module docstring."""
    file_content = """
# This is a comment
# Another comment
\"\"\"Module docstring\"\"\"
"""
    p = tmp_path / "comments.py"
    p.write_text(file_content)
    result = parse_python_file(str(p))
    assert result == "" # AST ignores comments and module docstrings if no definitions

def test_parse_python_file_non_existent(tmp_path):
    """Test parsing a non-existent Python file."""
    non_existent_path = tmp_path / "non_existent.py"
    result = parse_python_file(str(non_existent_path))
    assert f"# Error parsing Python file non_existent.py: [Errno 2] No such file or directory" in result

def test_parse_python_file_syntax_error(tmp_path):
    """Test parsing a Python file with a syntax error."""
    file_content = """
def func(
    pass
"""
    p = tmp_path / "syntax_error.py"
    p.write_text(file_content)
    result = parse_python_file(str(p))
    assert "Error parsing Python file syntax_error.py:" in result

def test_parse_python_file_no_docstrings(tmp_path):
    """Test parsing a Python file with no docstrings."""
    file_content = """
class NoDocClass:
    def no_doc_method(self):
        pass

def no_doc_func():
    pass
"""
    expected_output = """class NoDocClass:
    def no_doc_method(self):
        ...

def no_doc_func():
    ..."""
    p = tmp_path / "no_doc.py"
    p.write_text(file_content)
    result = parse_python_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_python_file_nested_structures(tmp_path):
    """
    Test parsing a Python file with nested structures.
    """
    file_content = """
class OuterClass:
    def outer_method(self):
        class InnerClass:
            def inner_method(self):
                pass
        def inner_function():
            pass
"""
    expected_output = """class OuterClass:
    def outer_method(self):
        ..."""
    p = tmp_path / "nested.py"
    p.write_text(file_content)
    result = parse_python_file(str(p))
    assert result.strip() == expected_output.strip()

# --- Tests for parse_js_ts_file ---

def test_parse_js_ts_file_simple(tmp_path):
    """Test parsing a simple JS/TS file with a class and a function."""
    file_content = """
/**
 * This is a class.
 */
class MyClass {
  /**
   * Constructor.
   */
  constructor(name) {
    this.name = name;
  }

  /**
   * A method.
   */
  myMethod() {
    console.log(this.name);
  }
}

/**
 * A simple function.
 * @param {string} arg1
 * @param {string} arg2
 */
function myFunction(arg1, arg2) {
  return arg1 + arg2;
}
"""
    expected_output = """/**
* This is a class.
*/
class MyClass {
/**
* Constructor.
*/
  constructor() { ... }
/**
* A method.
*/
  myMethod() { ... }
/**
* A simple function.
* @param {string} arg1
* @param {string} arg2
*/
function myFunction() { ... }"""
    
    p = tmp_path / "test.js"
    p.write_text(file_content)
    
    result = parse_js_ts_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_js_ts_file_async_exports(tmp_path):
    """Test parsing a JS/TS file with async functions/methods and exports."""
    file_content = """
export async function fetchData(url: string): Promise<any> {
  const response = await fetch(url);
  return response.json();
}

export default class Service {
  private async _privateMethod() {
    // ...
  }

  public async publicMethod() {
    // ...
  }
}
"""
    expected_output = """class Service {"""
    
    p = tmp_path / "test.ts"
    p.write_text(file_content)
    
    result = parse_js_ts_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_js_ts_file_empty(tmp_path):
    """Test parsing an empty JS/TS file."""
    p = tmp_path / "empty.js"
    p.write_text("")
    result = parse_js_ts_file(str(p))
    assert result == ""

def test_parse_js_ts_file_comments_only(tmp_path):
    """Test parsing a JS/TS file with only comments."""
    file_content = """
// Single line comment
/* Multi-line comment */
/** JSDoc block */
"""
    p = tmp_path / "comments.js"
    p.write_text(file_content)
    result = parse_js_ts_file(str(p))
    assert result == ""

def test_parse_js_ts_file_non_existent(tmp_path):
    """Test parsing a non-existent JS/TS file."""
    non_existent_path = tmp_path / "non_existent.js"
    result = parse_js_ts_file(str(non_existent_path))
    assert f"# Error reading JS/TS file non_existent.js: [Errno 2] No such file or directory" in result

def test_parse_js_ts_file_no_docblocks(tmp_path):
    """Test parsing a JS/TS file with no docblocks."""
    file_content = """
class NoDocClass {
  noDocMethod() {
    // ...
  }
}

function noDocFunc() {
  // ...
}
"""
    expected_output = """class NoDocClass {
  noDocMethod() { ... }
function noDocFunc() { ... }"""
    p = tmp_path / "no_doc.js"
    p.write_text(file_content)
    result = parse_js_ts_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_js_ts_file_keyword_methods(tmp_path):
    """Test parsing a JS/TS file with method names that could be keywords."""
    file_content = """
class MyClass {
  ifCondition() { /* ... */ }
  forLoop() { /* ... */ }
  whileLoop() { /* ... */ }
  switchCase() { /* ... */ }
  catchError() { /* ... */ }
  validMethod() { /* ... */ }
}
"""
    expected_output = """class MyClass {
  ifCondition() { ... }
  forLoop() { ... }
  whileLoop() { ... }
  switchCase() { ... }
  catchError() { ... }
  validMethod() { ... }"""
    p = tmp_path / "keywords.js"
    p.write_text(file_content)
    result = parse_js_ts_file(str(p))
    assert result.strip() == expected_output.strip()

def test_parse_js_ts_file_various_declarations(tmp_path):
    """Test parsing a JS/TS file with various class/function declarations."""
    file_content = """
class RegularClass {}
export class ExportedClass {}
export default class DefaultExportClass {}

function regularFunc() {}
export function exportedFunc() {}
export default function defaultExportFunc() {}

const arrowFunc = () => {}; // Should not be captured by current regex
let obj = {
    methodA() {},
    methodB: () => {}
}; // Should not be captured by current regex
"""
    expected_output = """class RegularClass {
class ExportedClass {
class DefaultExportClass {
function regularFunc() { ... }
function exportedFunc() { ... }
function defaultExportFunc() { ... }
  methodA() { ... }"""
    p = tmp_path / "various.ts"
    p.write_text(file_content)
    result = parse_js_ts_file(str(p))
    assert result.strip() == expected_output.strip()

# --- Tests for compact_directory ---

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_happy_path(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting a directory with mixed Python and JS/TS files."""
    # Setup dummy files
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "sub").mkdir()
    
    py_file1 = tmp_path / "src" / "file1.py"
    py_file1.write_text("def func1(): pass")
    
    js_file1 = tmp_path / "src" / "file2.js"
    js_file1.write_text("function func2() {}")
    
    ts_file1 = tmp_path / "src" / "sub" / "file3.ts"
    ts_file1.write_text("class MyClass {}")
    
    txt_file = tmp_path / "src" / "notes.txt"
    txt_file.write_text("some notes") # Should be ignored
    
    # Mock the parsing functions
    mock_parse_python.return_value = "Python content for func1"
    mock_parse_js_ts.side_effect = ["JS content for func2", "TS content for MyClass"]
    
    expected_output_parts = [
        "File: src/file1.py (Python)\n" + "=" * 40,
        "Python content for func1",
        "\n",
        "File: src/file2.js (JavaScript/TypeScript)\n" + "=" * 40,
        "JS content for func2",
        "\n",
        "File: src/sub/file3.ts (JavaScript/TypeScript)\n" + "=" * 40,
        "TS content for MyClass",
    ]
    expected_output = "\n".join(expected_output_parts)
    
    result = compact_directory(str(tmp_path), [])
    
    assert result.replace("\\", "/").strip() == expected_output.strip()
    
    mock_parse_python.assert_called_once_with(str(py_file1))
    assert mock_parse_js_ts.call_count == 2
    mock_parse_js_ts.assert_any_call(str(js_file1))
    mock_parse_js_ts.assert_any_call(str(ts_file1))

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_exclude_patterns(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting a directory with custom exclude patterns."""
    (tmp_path / "app_dir").mkdir()
    (tmp_path / "build").mkdir()
    (tmp_path / "node_modules").mkdir() # This is a default exclude, but also test custom
    
    py_file = tmp_path / "app_dir" / "app.py"
    py_file.write_text("...")
    
    test_py_file = tmp_path / "app_dir" / "test_app.py"
    test_py_file.write_text("...")
    
    build_js_file = tmp_path / "build" / "main.js"
    build_js_file.write_text("...")
    
    node_module_ts_file = tmp_path / "node_modules" / "lib" / "index.ts"
    os.makedirs(os.path.dirname(node_module_ts_file), exist_ok=True)
    node_module_ts_file.write_text("...")
    
    mock_parse_python.return_value = "Python app content"
    mock_parse_js_ts.return_value = "JS build content"
    
    exclude_patterns = ["test", "build"] # 'node_modules' is already excluded by default
    
    result = compact_directory(str(tmp_path), exclude_patterns)
    
    expected_output_parts = [
        "File: app_dir/app.py (Python)\n" + "=" * 40,
        "Python app content",
        ""
    ]
    expected_output = "\n".join(expected_output_parts)
    
    assert result.replace("\\", "/").strip() == expected_output.strip()
    
    mock_parse_python.assert_called_once_with(str(py_file))
    mock_parse_js_ts.assert_not_called() # build_js_file and node_module_ts_file should be excluded

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_empty_directory(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting an empty directory."""
    result = compact_directory(str(tmp_path), [])
    assert result == ""
    mock_parse_python.assert_not_called()
    mock_parse_js_ts.assert_not_called()

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_only_excluded_files(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting a directory where all files are excluded."""
    (tmp_path / "test_dir").mkdir()
    (tmp_path / "test_dir" / "test_file.py").write_text("...")
    (tmp_path / "test_dir" / "build_file.js").write_text("...")
    
    exclude_patterns = ["test", "build"]
    
    result = compact_directory(str(tmp_path), exclude_patterns)
    assert result == ""
    mock_parse_python.assert_not_called()
    mock_parse_js_ts.assert_not_called()

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_non_existent_directory(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting a non-existent directory."""
    non_existent_dir = tmp_path / "non_existent"
    result = compact_directory(str(non_existent_dir), [])
    assert result == "" # os.walk on non-existent dir yields nothing
    mock_parse_python.assert_not_called()
    mock_parse_js_ts.assert_not_called()

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_other_file_types(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test compacting a directory with only non-Python/JS/TS files."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "file.txt").write_text("text content")
    (tmp_path / "src" / "image.png").write_bytes(b"binary content")
    
    result = compact_directory(str(tmp_path), [])
    assert result == ""
    mock_parse_python.assert_not_called()
    mock_parse_js_ts.assert_not_called()

@patch('compactor.parse_python_file')
@patch('compactor.parse_js_ts_file')
def test_compact_directory_default_excludes(mock_parse_js_ts, mock_parse_python, tmp_path):
    """Test that default excluded directories are skipped."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / "build").mkdir()

    (tmp_path / ".git" / "config").write_text("...")
    (tmp_path / "node_modules" / "lib.js").write_text("...")
    (tmp_path / "__pycache__" / "module.pyc").write_bytes(b"...")
    (tmp_path / "dist" / "bundle.js").write_text("...")
    (tmp_path / "build" / "index.html").write_text("...")
    
    (tmp_path / "app.py").write_text("def app(): pass")
    mock_parse_python.return_value = "App content"

    result = compact_directory(str(tmp_path), [])
    
    expected_output_parts = [
        "File: app.py (Python)\n" + "=" * 40,
        "App content",
        ""
    ]
    expected_output = "\n".join(expected_output_parts)
    
    assert result.strip() == expected_output.strip()
    mock_parse_python.assert_called_once_with(str(tmp_path / "app.py"))
    mock_parse_js_ts.assert_not_called()

# --- Tests for main ---

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('compactor.compact_directory')
@patch('builtins.open', new_callable=mock_open)
@patch('sys.exit')
@patch('builtins.print')
def test_main_happy_path(mock_print, mock_sys_exit, mock_file_open, mock_compact_directory, mock_isdir, mock_parse_args):
    """Test main function with valid inputs and successful execution."""
    mock_parse_args.return_value = MagicMock(
        directory="/test/dir",
        output="/test/output.txt",
        exclude="test,build"
    )
    mock_isdir.return_value = True
    mock_compact_directory.return_value = "Compacted content here"
    
    main()
    
    mock_isdir.assert_called_once_with("/test/dir")
    mock_compact_directory.assert_called_once_with("/test/dir", ["test", "build"])
    
    mock_file_open.assert_called_once_with("/test/output.txt", "w", encoding="utf-8")
    mock_file_open().write.assert_called_once_with("Compacted content here")
    
    mock_print.assert_any_call("Scanning directory: /test/dir...")
    mock_print.assert_any_call("\n[SUCCESS] Compaction completed!")
    mock_print.assert_any_call("Summary saved at: /test/output.txt")
    mock_sys_exit.assert_not_called()

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('sys.exit')
@patch('builtins.print')
def test_main_directory_not_exist(mock_print, mock_sys_exit, mock_isdir, mock_parse_args):
    """Test main function when the input directory does not exist."""
    mock_parse_args.return_value = MagicMock(
        directory="/non/existent/dir",
        output="/test/output.txt",
        exclude=""
    )
    mock_isdir.return_value = False
    mock_sys_exit.side_effect = SystemExit
    
    with pytest.raises(SystemExit):
        main()
    
    mock_isdir.assert_called_once_with("/non/existent/dir")
    mock_print.assert_called_once_with("Error: Directory does not exist: /non/existent/dir", file=sys.stderr)
    mock_sys_exit.assert_called_once_with(1)

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('compactor.compact_directory')
@patch('builtins.open', new_callable=mock_open)
@patch('sys.exit')
@patch('builtins.print')
def test_main_output_file_write_error(mock_print, mock_sys_exit, mock_file_open, mock_compact_directory, mock_isdir, mock_parse_args):
    """Test main function when there's an error writing the output file."""
    mock_parse_args.return_value = MagicMock(
        directory="/test/dir",
        output="/invalid/path/output.txt",
        exclude=""
    )
    mock_isdir.return_value = True
    mock_compact_directory.return_value = "Compacted content"
    
    mock_file_open.side_effect = IOError("Permission denied")
    mock_sys_exit.side_effect = SystemExit
    
    with pytest.raises(SystemExit):
        main()
    
    mock_isdir.assert_called_once_with("/test/dir")
    mock_compact_directory.assert_called_once_with("/test/dir", [""])
    mock_file_open.assert_called_once_with("/invalid/path/output.txt", "w", encoding="utf-8")
    
    mock_print.assert_any_call("Error writing output file: Permission denied", file=sys.stderr)
    mock_sys_exit.assert_called_once_with(1)

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('compactor.compact_directory')
@patch('builtins.open', new_callable=mock_open)
@patch('sys.exit')
@patch('builtins.print')
def test_main_empty_exclude(mock_print, mock_sys_exit, mock_file_open, mock_compact_directory, mock_isdir, mock_parse_args):
    """Test main function with an empty exclude pattern."""
    mock_parse_args.return_value = MagicMock(
        directory="/test/dir",
        output="/test/output.txt",
        exclude=""
    )
    mock_isdir.return_value = True
    mock_compact_directory.return_value = "Compacted content"
    
    main()
    
    mock_compact_directory.assert_called_once_with("/test/dir", [""]) # Empty string becomes an element
    mock_sys_exit.assert_not_called()

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('compactor.compact_directory')
@patch('builtins.open', new_callable=mock_open)
@patch('sys.exit')
@patch('builtins.print')
def test_main_multiple_exclude_patterns(mock_print, mock_sys_exit, mock_file_open, mock_compact_directory, mock_isdir, mock_parse_args):
    """Test main function with multiple exclude patterns."""
    mock_parse_args.return_value = MagicMock(
        directory="/test/dir",
        output="/test/output.txt",
        exclude="test,build,docs"
    )
    mock_isdir.return_value = True
    mock_compact_directory.return_value = "Compacted content"
    
    main()
    
    mock_compact_directory.assert_called_once_with("/test/dir", ["test", "build", "docs"])
    mock_sys_exit.assert_not_called()

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isdir')
@patch('compactor.compact_directory')
@patch('builtins.open', new_callable=mock_open)
@patch('sys.exit')
@patch('builtins.print')
def test_main_compact_directory_returns_error_string(mock_print, mock_sys_exit, mock_file_open, mock_compact_directory, mock_isdir, mock_parse_args):
    """Test main function when compact_directory returns an error string."""
    mock_parse_args.return_value = MagicMock(
        directory="/test/dir",
        output="/test/output.txt",
        exclude=""
    )
    mock_isdir.return_value = True
    mock_compact_directory.return_value = "# Error parsing file: Some error"
    
    main()
    
    mock_file_open.assert_called_once_with("/test/output.txt", "w", encoding="utf-8")
    mock_file_open().write.assert_called_once_with("# Error parsing file: Some error")
    mock_print.assert_any_call("\n[SUCCESS] Compaction completed!") # Still success from main's perspective
    mock_print.assert_any_call("Summary saved at: /test/output.txt")
    mock_sys_exit.assert_not_called()
