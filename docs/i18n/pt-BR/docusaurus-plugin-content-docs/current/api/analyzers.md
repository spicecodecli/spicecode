---
sidebar_position: 3
---

# API Reference: Analyzers Module (`spice/analyzers`)

The `spice/analyzers` module is where the core logic for extracting metrics and insights from the parsed source code resides. After the `lexers` module tokenizes the code and the `parser` module constructs an Abstract Syntax Tree (AST) or similar structured representation, the individual analyzer components within this module are invoked. Each analyzer is designed to traverse the AST (or work with the token stream directly for simpler metrics) and calculate specific characteristics of the code. They embody the specialized senses of SpiceCode, each focused on detecting a particular aspect of code quality, structure, or style.

## Purpose of Code Analysis

While the parser verifies the grammatical correctness of the code, the analyzers perform semantic analysis and metric calculation. They examine the structure represented by the AST to understand *what* the code does and *how* it is written. The goal is to produce objective measurements and qualitative assessments that help developers understand maintainability, complexity, adherence to conventions, and potential areas for improvement.

## Structure of the `spice/analyzers` Module

The `spice/analyzers` directory contains individual Python files, each typically implementing a specific analysis metric or a closely related group of metrics:

```
spice/
├── __init__.py
├── analyze.py      # Main analysis orchestration logic?
└── analyzers/
    ├── __init__.py
    ├── count_comment_lines.py
    ├── count_comment_ratio.py
    ├── count_external_dependencies.py
    ├── count_functions.py
    ├── count_inline_comments.py
    ├── count_lines.py
    ├── count_method_type.py
    └── indentation.py
```

### `analyze.py` (within `spice/`)

While not strictly inside the `analyzers` subdirectory, the `analyze.py` file likely plays a crucial role in orchestrating the analysis process. It might contain the main function or class that:

1.  Takes the file path as input.
2.  Invokes the appropriate lexer and parser based on the language.
3.  Receives the resulting AST or token stream.
4.  Instantiates and runs the relevant analyzers from the `spice/analyzers` directory, passing the AST/tokens to them.
5.  Collects the results from each analyzer.
6.  Formats and returns the final analysis report (either for display, JSON output, or export).

### Individual Analyzer Files (within `spice/analyzers/`)

Each `.py` file within the `spice/analyzers` subdirectory represents a distinct analysis capability. Examples include:

*   **`count_lines.py`:** Implements the logic to count total, code, and blank lines, likely by processing the raw source text or token stream.
*   **`count_comment_lines.py`, `count_inline_comments.py`, `count_comment_ratio.py`:** These implement the various comment-related metrics. They would typically traverse the AST or token stream, identifying comment nodes/tokens and comparing their counts/positions relative to code lines.
*   **`count_functions.py`:** Traverses the AST to find and count nodes representing function or method definitions (e.g., `FunctionDefinition` nodes).
*   **`count_method_type.py`:** Analyzes function/method definition nodes in the AST to categorize them based on language-specific features (e.g., class methods, static methods, constructors).
*   **`count_external_dependencies.py`:** Scans the AST for import/require/use statements to identify and count external dependencies.
*   **`indentation.py`:** Analyzes the token stream or AST to check for consistent use of whitespace for indentation, flagging inconsistencies based on language conventions.

Each analyzer file typically defines a function or class that takes the AST (or token stream/source text) as input and returns the calculated metric(s). They often rely on traversing the AST structure using patterns like the Visitor pattern to efficiently inspect relevant nodes.

## Usage within SpiceCode

When the `spice analyze` or `spice export` command is executed, the main analysis orchestrator (`spice/analyze.py`) identifies the language, parses the code, and then invokes the appropriate set of analyzers from this directory. If the user selected specific analyses interactively, only those corresponding analyzers are run. If `--all` is used or the command is `export`, all applicable analyzers for the language are executed.

The results from each analyzer are collected and aggregated into a final report, which is then presented to the user or saved to a file in the specified format.

This modular structure makes the analysis framework extensible. Adding a new analysis metric typically involves creating a new Python file within the `spice/analyzers` directory, implementing the logic to calculate the metric (usually by traversing the AST), and integrating it into the orchestration process in `spice/analyze.py`. This design promotes separation of concerns and makes it easier to maintain and enhance SpiceCode's analytical capabilities.
