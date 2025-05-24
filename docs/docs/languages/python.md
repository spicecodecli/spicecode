---
sidebar_position: 3
---

# Python Language Support

SpiceCode provides first-class, native support for analyzing Python source code files, which conventionally use the `.py` extension. As Python continues to be a dominant language in diverse fields like web development, data science, scripting, and automation, SpiceCode includes a meticulously crafted lexer and parser specifically designed to handle Python's syntax, including its significant whitespace rules. This built-in capability allows for deep and accurate analysis of Python code without requiring external Python interpreters or analysis libraries, ensuring a self-contained and consistent analysis process, much like the Fremen rely on their deep-seated understanding of Arrakis' ecology.

## Native Lexer and Parser

The foundation of Python support within SpiceCode is its custom lexer (`pythonlexer.py` found in `lexers/python`) and the associated parsing logic. This native implementation is carefully constructed to tokenize Python code correctly, recognizing keywords, identifiers, operators, literals (strings, numbers, lists, tuples, dictionaries, etc.), and comments (`#`). Crucially, it also handles Python's indentation rules, which define code blocks. The parser uses this token stream to build an internal representation of the Python code's structure, enabling effective analysis by the various SpiceCode modules.

This native approach yields significant benefits:

1.  **Accuracy:** The lexer and parser are specifically designed for Python 3 syntax, leading to precise understanding of code structure, including indentation sensitivity.
2.  **Independence:** SpiceCode can analyze `.py` files without needing a Python interpreter installed on the system (beyond the Python environment needed to run SpiceCode itself) or relying on external Python static analysis tools.
3.  **Consistency:** The analysis methodology remains uniform with other languages supported by SpiceCode, providing a cohesive user experience.

## Applicable Analyzers

Nearly all of SpiceCode's standard analyzers are applicable to Python code, leveraging the detailed structural information provided by the native lexer and parser. When analyzing a `.py` file, you can expect insights from analyzers such as:

*   **Line Counts (`count_lines`):** Provides the standard breakdown of total, code, and blank lines.
*   **Comment Analysis (`count_comment_lines`, `count_inline_comments`, `count_comment_ratio`):** Analyzes the usage and density of `#` comments.
*   **Function and Method Analysis (`count_functions`, `count_method_type`):** Counts `def` statements (functions and methods) and potentially analyzes characteristics like class methods, static methods, or dunder methods based on naming conventions.
*   **Dependency Analysis (`count_external_dependencies`):** Counts `import` and `from ... import` statements to gauge the reliance on external or standard library modules.
*   **Indentation Analysis (`indentation`):** Critically important for Python, this analyzer verifies the consistency of indentation (typically 4 spaces per level) used for defining code blocks.

## Example Analysis

Let's consider a simple Python file, `utils.py`:

```python
# Utility functions for data processing
import json

DEFAULT_FACTOR = 10

def process_data(data, factor=None): # Process incoming data
    """Processes the input data using a factor."""
    if factor is None:
        factor = DEFAULT_FACTOR
    
    processed = [item * factor for item in data]
    # Log processing (example)
    print(f"Processed {len(data)} items with factor {factor}")
    return processed

class DataHandler:
    def __init__(self, source_file):
        self.source = source_file
        self.data = self._load_data()

    def _load_data(self):
        # Private helper method to load data
        try:
            with open(self.source, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found - {self.source}")
            return []

    def run_processing(self, factor=None):
        return process_data(self.data, factor)

```

Running `spice analyze utils.py --all` would engage the Python lexer and parser. The analyzers would then report on line counts, comment usage (including docstrings and inline comments), the number of functions/methods (`process_data`, `__init__`, `_load_data`, `run_processing`), the external dependency (`json`), and the consistency of indentation throughout the file.

Exporting these findings, for example, to CSV:

```bash
spice export utils.py --format csv --output utils_metrics.csv
```

This command would generate a `utils_metrics.csv` file containing the structured analysis results, suitable for import into spreadsheets or databases.

SpiceCode's robust, native support for Python allows developers to seamlessly integrate detailed code analysis into their Python workflows, promoting higher code quality, better maintainability, and adherence to best practices within their Python projects.
