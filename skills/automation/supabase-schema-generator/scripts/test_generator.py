import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add generator directory to path so we can import it
sys.path.append(os.path.dirname(__file__))
import generator

class TestSupabaseSchemaGenerator(unittest.TestCase):
    def test_clean_code_blocks(self):
        text_with_blocks = "```typescript\nconst a = 1;\n```"
        self.assertEqual(generator.clean_code_blocks(text_with_blocks), "const a = 1;")
        
        text_without_blocks = "const a = 1;"
        self.assertEqual(generator.clean_code_blocks(text_without_blocks), "const a = 1;")

    @patch("os.environ.get")
    def test_get_api_key_from_env(self, mock_env_get):
        mock_env_get.side_effect = lambda key: "mock-api-key" if key in ("GEMINI_API_KEY", "GOOGLE_API_KEY") else None
        self.assertEqual(generator.get_api_key(), "mock-api-key")

    @patch("os.environ.get")
    @patch("generator.open", new_callable=mock_open, read_data="GOOGLE_API_KEY=mock-env-file-key\n")
    def test_get_api_key_from_file_fallback(self, mock_file_open, mock_env_get):
        mock_env_get.return_value = None
        self.assertEqual(generator.get_api_key(), "mock-env-file-key")
        mock_file_open.assert_called_once_with(r"C:\Users\araga\.hermes\.env", "r", encoding="utf-8")

    @patch("os.path.exists")
    @patch("generator.open", new_callable=mock_open, read_data="CREATE TABLE test (id INT);")
    @patch("generator.get_api_key")
    @patch("generator.genai.Client")
    @patch("generator.analyze_schema")
    @patch("sys.exit")
    def test_main_success(self, mock_exit, mock_analyze, mock_client_class, mock_get_api_key, mock_file_open, mock_exists):
        mock_exists.return_value = True
        mock_get_api_key.return_value = "mock-key"
        
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_analyze.return_value = "[TYPESCRIPT_TYPES]\nexport interface Test {}\n[RLS_POLICIES]\nALTER TABLE test ENABLE RLS;"
        
        test_args = ["generator.py", "--schema", "dummy.sql", "--output-types", "types.ts", "--output-rls", "policies.sql"]
        with patch.object(sys, "argv", test_args):
            generator.main()

        # Check files were written
        mock_file_open.assert_any_call("dummy.sql", "r", encoding="utf-8")
        mock_file_open.assert_any_call("types.ts", "w", encoding="utf-8")
        mock_file_open.assert_any_call("policies.sql", "w", encoding="utf-8")
        
        mock_exit.assert_not_called()

    @patch("os.path.exists")
    def test_main_schema_not_found(self, mock_exists):
        mock_exists.return_value = False
        
        test_args = ["generator.py", "--schema", "missing.sql"]
        with patch.object(sys, "argv", test_args):
            with self.assertRaises(SystemExit) as cm:
                generator.main()
            self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
