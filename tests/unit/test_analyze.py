import os
import unittest
from spice.analyze import analyze_file

#python -m unittest discover tests/unit -v


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        # caminho para a pasta de arquivos de exemplo
        self.sample_files_dir = os.path.join(os.path.dirname(__file__), "sample_files")

    def test_count_lines(self):
        # testa a contagem de linhas para um arquivo Python
        file_path = os.path.join(self.sample_files_dir, "example.py")
        results = analyze_file(file_path, selected_stats=["line_count"])
        self.assertEqual(results["line_count"], 10)  

    def test_count_functions_python(self):
        # testa a contagem de funções para um arquivo Python
        file_path = os.path.join(self.sample_files_dir, "example.py")
        results = analyze_file(file_path, selected_stats=["function_count"])
        self.assertEqual(results["function_count"], 3)

    def test_count_functions_javascript(self):
        # testa a contagem de funções para um arquivo JavaScript
        file_path = os.path.join(self.sample_files_dir, "example.js")
        results = analyze_file(file_path, selected_stats=["function_count"])
        self.assertEqual(results["function_count"], 2)

    def test_count_comment_lines_ruby(self):
        # testa a contagem de linhas de comentário para um arquivo Ruby
        file_path = os.path.join(self.sample_files_dir, "example.rb")
        results = analyze_file(file_path, selected_stats=["comment_line_count"])
        self.assertEqual(results["comment_line_count"], 2)

    def test_count_comment_lines_go(self):
        # testa a contagem de linhas de comentário para um arquivo Go
        file_path = os.path.join(self.sample_files_dir, "example.go")
        results = analyze_file(file_path, selected_stats=["comment_line_count"])
        self.assertEqual(results["comment_line_count"], 11)

    def test_unsupported_file_extension(self):
        # Testa o tratamento de extensões de arquivo não suportadas
        file_path = os.path.join(self.sample_files_dir, "example.txt")
        with self.assertRaises(ValueError):
            analyze_file(file_path)

    def test_all_stats(self):
        # testa a análise completa (todas as estatísticas) para um arquivo Python
        file_path = os.path.join(self.sample_files_dir, "example.py")
        results = analyze_file(file_path)
        self.assertIn("line_count", results)
        self.assertIn("function_count", results)
        self.assertIn("comment_line_count", results)

if __name__ == "__main__":
    unittest.main()