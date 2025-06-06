---
sidebar_position: 2
---

# API Reference: Parser Module (`parser`)

Following the lexical analysis phase performed by the `lexers` module, the resulting stream of tokens is passed to the `parser` module. This module is responsible for syntactic analysis – the process of analyzing the sequence of tokens to determine the grammatical structure of the source code according to the rules of the specific programming language. The parser effectively checks if the token stream forms a valid program and typically constructs a data structure, often an Abstract Syntax Tree (AST), that represents the hierarchical structure of the code. This structured representation is crucial for the subsequent semantic analysis and metric calculation performed by the `spice/analyzers`.

Similar to the lexers, SpiceCode employs a native parsing approach, meaning it does not rely on external parsing libraries or language-specific compilers to generate ASTs. This ensures self-sufficiency and allows for tailored parsing logic suited to SpiceCode's specific analysis needs.

## Purpose of Syntactic Analysis

Syntactic analysis, or parsing, takes the flat sequence of tokens from the lexer and organizes them into a hierarchical structure that reflects the code's logical organization. It verifies that the code adheres to the language's grammar rules (e.g., ensuring parentheses are balanced, statements are correctly formed, keywords are used appropriately). The primary output of this phase in many compilers and analysis tools is an AST. An AST abstracts away much of the source code's superficial syntax (like parentheses or commas) and represents the essential structural elements (like function definitions, loops, conditional statements, expressions) and their relationships.

## Structure of the `parser` Module

The `parser` module within SpiceCode likely contains the core parsing logic and potentially definitions for the AST nodes:

```
parser/
├── __init__.py
├── ast.py        # Defines the nodes for the Abstract Syntax Tree (AST)
└── parser.py     # Contains the main Parser class and parsing logic
```

### `ast.py`

This file is expected to define the various types of nodes that make up the Abstract Syntax Tree. An AST is a tree representation of the code's structure. Each node in the tree represents a construct occurring in the source code. For example, there might be node classes for:

*   **Program/Module:** The root node representing the entire file.
*   **FunctionDefinition:** Representing a function or method definition, potentially containing nodes for parameters, return type, and the function body.
*   **ClassDefinition:** Representing a class definition.
*   **IfStatement:** Representing an if-else conditional structure.
*   **ForLoop/WhileLoop:** Representing loop constructs.
*   **Assignment:** Representing an assignment operation.
*   **VariableDeclaration:** Representing variable declarations.
*   **Expression Nodes:** Representing various kinds of expressions (e.g., BinaryOperation, FunctionCall, Literal, VariableReference).

Each AST node class would typically store relevant information about the construct it represents (e.g., a FunctionDefinition node might store the function name, parameter list, and a list of statements in its body).

### `parser.py`

This file likely contains the main `Parser` class (or equivalent logic). The parser takes the stream of tokens generated by a language-specific lexer as input. It implements parsing algorithms (e.g., recursive descent, or using a parser generator pattern) to consume the tokens and build the AST according to the grammar rules of the target language.

The parser needs to handle the specific syntax of each supported language (Go, JavaScript, Python, Ruby). This might involve:

*   A single `Parser` class with methods that adapt based on the detected language.
*   Or potentially separate parser implementations or configurations for each language, although the file structure suggests a more unified approach.

The parser interacts closely with the `ast.py` module, creating instances of the appropriate AST node classes as it recognizes grammatical structures in the token stream. It also performs error handling, reporting syntax errors if the token sequence violates the language's grammar rules.

## Usage within SpiceCode

After a lexer tokenizes the input source file, the `parser` module is invoked with this token stream. The parser constructs the AST. This AST is then passed to the various analyzers located in the `spice/analyzers` directory. The analyzers traverse this AST, extracting information and calculating metrics based on the structure and content represented by the tree nodes. For example, the `count_functions` analyzer would traverse the AST looking for `FunctionDefinition` nodes.

The `parser` module, along with the `ast.py` definitions, forms the bridge between the raw text of the source code and the structured understanding required for meaningful analysis. Its native implementation is key to SpiceCode's self-contained nature and its ability to provide consistent analysis across different programming languages.
