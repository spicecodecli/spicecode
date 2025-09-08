---
sidebar_position: 1
---

# Go Language Support

SpiceCode provides robust, native support for analyzing Go (Golang) source code files, typically identified by the `.go` extension. Recognizing Go's increasing popularity for building efficient and concurrent systems, SpiceCode includes a dedicated lexer and parser specifically designed to understand Go's syntax and structure. This allows for accurate and insightful analysis without relying on external tools or libraries, ensuring a self-contained and consistent experience, much like the Fremen rely on their own deep knowledge of the desert rather than off-world technologies.

## Native Lexer and Parser

The cornerstone of Go support in SpiceCode is its custom-built lexer (`golexer.py` within the `lexers/golang` directory) and the corresponding parsing logic integrated into the main parser module. This native implementation meticulously processes Go source code, tokenizing keywords, identifiers, operators, literals, and comments according to the Go language specification. The parser then constructs an internal representation (like an Abstract Syntax Tree or similar structure) of the code, enabling the various analyzers to operate effectively.

This native approach offers several advantages:

1.  **Accuracy:** The lexer and parser are tailored specifically for Go syntax, leading to more precise analysis compared to generic tools.
2.  **Independence:** SpiceCode does not require users to have Go compilers or external Go analysis tools installed on their system to analyze `.go` files.
3.  **Consistency:** The analysis process remains consistent with how other languages are handled within SpiceCode, providing a unified user experience.

## Applicable Analyzers

Most of SpiceCode's standard analyzers are applicable to Go code, leveraging the output of the native lexer and parser. When you analyze a `.go` file, you can expect metrics from analyzers such as:

*   **Line Counts (`count_lines`):** Provides total, code, and blank line counts.
*   **Comment Analysis (`count_comment_lines`, `count_inline_comments`, `count_comment_ratio`):** Analyzes single-line (`//`) and multi-line (`/* ... */`) comments, including their ratio to code lines.
*   **Function Analysis (`count_functions`):** Identifies and counts `func` declarations.
*   **Dependency Analysis (`count_external_dependencies`):** Counts `import` statements to gauge reliance on external packages.
*   **Indentation Analysis (`indentation`):** Checks for consistent use of tabs (standard in Go) for indentation.

Specific analyzers like `count_method_type` might have Go-specific interpretations, potentially distinguishing between regular functions and methods associated with structs.

## Example Analysis

Consider a simple Go file named `hello.go`:

```go
package main

import "fmt"

// Greet generates a greeting message.
func Greet(name string) string {
	// Return a formatted string
	return fmt.Sprintf("Hello, %s! Welcome from Go.", name)
}

func main() {
	message := Greet("Go Developer")
	fmt.Println(message) // Print the greeting
}
```

Running `spice analyze hello.go --all` would invoke the Go lexer and parser, followed by the applicable analyzers. The output would provide metrics detailing line counts, comment statistics (including the function comment and inline comments), the number of functions (`Greet` and `main`), the number of external dependencies (`fmt`), and indentation consistency.

Similarly, `spice export hello.go --format json --output hello_report.json` would generate a structured JSON report containing these metrics.

SpiceCode's dedicated support for Go ensures that developers working with this powerful language can benefit from the same level of detailed analysis and insight available for other supported languages, helping maintain code quality and consistency within their Go projects.
