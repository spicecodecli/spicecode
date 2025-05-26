---
sidebar_position: 2
---

# JavaScript Language Support

SpiceCode offers comprehensive, native analysis capabilities for JavaScript code, commonly found in files with the `.js` extension. As JavaScript remains a cornerstone of web development and beyond, SpiceCode incorporates a dedicated lexer and parser specifically engineered to handle its dynamic nature and syntax nuances. This built-in support ensures that JavaScript projects can be analyzed accurately and efficiently without external dependencies, providing developers with valuable insights derived directly from their source code, much like a Fremen relies on their innate understanding of the desert rhythms.

## Native Lexer and Parser

At the heart of SpiceCode's JavaScript support is its custom lexer (`javascriptlexer.py` located in `lexers/javascript`) and the integrated parsing logic. This native implementation is designed to tokenize JavaScript code accurately, recognizing keywords, identifiers, operators, literals (including string, number, boolean, null, undefined, regex), and comments (both single-line `//` and multi-line `/* ... */`). The parser subsequently builds an internal representation of the code structure, which serves as the foundation for the various analysis modules.

Key benefits of this native approach include:

1.  **Precision:** Tailored specifically for JavaScript syntax (including common ES features), leading to more reliable analysis than generic tools might provide.
2.  **Self-Sufficiency:** SpiceCode analyzes `.js` files directly without needing Node.js or other JavaScript runtimes/tools installed on the system.
3.  **Uniformity:** The analysis process aligns with how SpiceCode handles other supported languages, offering a consistent user experience across different codebases.

## Applicable Analyzers

The majority of SpiceCode's standard analyzers are fully compatible with JavaScript code, utilizing the detailed information provided by the native lexer and parser. When analyzing a `.js` file, you can leverage analyzers such as:

*   **Line Counts (`count_lines`):** Delivers total, code, and blank line metrics.
*   **Comment Analysis (`count_comment_lines`, `count_inline_comments`, `count_comment_ratio`):** Quantifies comment usage and density.
*   **Function Analysis (`count_functions`):** Counts `function` declarations, function expressions, and potentially arrow functions, depending on implementation depth.
*   **Dependency Analysis (`count_external_dependencies`):** Identifies and counts `require()` calls or `import` statements to assess external module usage.
*   **Indentation Analysis (`indentation`):** Checks for consistent indentation patterns (commonly spaces in JavaScript development).
*   **Method Type Analysis (`count_method_type`):** May distinguish between regular functions, methods within classes, constructors, etc., providing insights into object-oriented or prototype-based structures.

## Example Analysis

Consider this simple JavaScript file, `calculator.js`:

```javascript
// Simple calculator functions

/* 
 * Adds two numbers.
 */
function add(a, b) {
    // Return the sum
    return a + b;
}

class Calculator {
    constructor() {
        this.result = 0;
    }

    // Method to multiply
    multiply(a, b) {
        this.result = a * b;
        return this.result; // Return calculation
    }
}

const sum = add(5, 3); // Example usage
console.log(`Sum: ${sum}`);

const calc = new Calculator();
console.log(`Product: ${calc.multiply(5, 3)}`);
```

Running `spice analyze calculator.js --all` would trigger the JavaScript lexer and parser. The subsequent analysis would yield metrics on line counts, comment types and ratio, the number of functions/methods (`add`, `constructor`, `multiply`), dependency counts (potentially identifying `require` or `import` if used), and indentation consistency.

Exporting these results, for instance to HTML:

```bash
spice export calculator.js --format html --output calculator_report.html
```

This would generate an HTML document detailing all the gathered metrics for easy viewing and sharing.

SpiceCode's dedicated JavaScript support empowers developers to apply consistent code analysis practices to their JavaScript projects, helping to ensure code quality, maintainability, and adherence to best practices within the dynamic world of JavaScript development.
