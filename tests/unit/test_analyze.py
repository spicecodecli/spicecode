import os
import unittest
from spice.analyze import analyze_file

class TestAnalyze(unittest.TestCase):
    def setUp(self):
        # caminho para a pasta de arquivos de exemplo
        self.sample_files = os.path.join(os.path.dirname(__file__), "sample_files")
        

    def test_count_lines(self):
        # testa a contagem de linhas para um arquivo Python
        file_path = os.path.join(self.sample_files, "example.py")
        results = analyze_file(file_path, selected_stats=["line_count"])
        self.assertEqual(results["line_count"], 161)

    def test_count_functions_python(self):
        # testa a contagem de funções para um arquivo Python
        file_path = os.path.join(self.sample_files, "example.py")
        results = analyze_file(file_path, selected_stats=["function_count"])
        self.assertEqual(results["function_count"], 17)

    def test_count_functions_javascript(self):
        # testa a contagem de funções para um arquivo JavaScript
        file_path = os.path.join(self.sample_files, "example.js")
        results = analyze_file(file_path, selected_stats=["function_count"])
        self.assertEqual(results["function_count"], 153)  
    def test_count_comment_lines_ruby(self):
        # testa a contagem de linhas de comentário para um arquivo Ruby
        file_path = os.path.join(self.sample_files, "example.rb")
        results = analyze_file(file_path, selected_stats=["comment_line_count"])
        self.assertEqual(results["comment_line_count"], 226)

    def test_count_comment_lines_go(self):
        # testa a contagem de linhas de comentário para um arquivo Go
        file_path = os.path.join(self.sample_files, "example.go")
        results = analyze_file(file_path, selected_stats=["comment_line_count"])
        self.assertEqual(results["comment_line_count"], 195)

    def test_all_stats(self):
        # testa a análise completa (todas as estatísticas) para um arquivo Python
        file_path = os.path.join(self.sample_files, "example.py")
        results = analyze_file(file_path)
        self.assertIn("line_count", results)
        self.assertIn("function_count", results)
        self.assertIn("comment_line_count", results)

if __name__ == "__main__":
    unittest.main()