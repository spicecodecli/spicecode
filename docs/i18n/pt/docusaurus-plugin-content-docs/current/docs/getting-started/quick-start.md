---
sidebar_position: 2
---

# Quick Start Guide

Now that SpiceCode is installed on your system, you are ready to take your first steps into analyzing code, much like a Fremen taking their initial strides across the vast desert sands under the twin moons of Arrakis. This quick start guide will walk you through the fundamental commands and demonstrate a basic analysis workflow, allowing you to quickly experience the core capabilities of SpiceCode.

## Verifying Your Setup

Before diving into analysis, it's always a good practice to ensure the tool is responding correctly. As covered in the installation guide, you can confirm SpiceCode is operational by checking its version:

```bash
spice version
```

This command should return the installed version number. Additionally, SpiceCode includes a simple greeting command, a ritualistic acknowledgment like a Fremen salute, which can also serve as a basic check:

```bash
spice hello
```

Executing this should display a welcoming message, confirming the CLI is responsive.

## Performing Your First Analysis

The primary function of SpiceCode is code analysis. Let's perform a basic analysis on a sample code file. If you don't have a readily available file in one of the supported languages (Python, JavaScript, Ruby, Go), you can quickly create one. For instance, create a simple Python file named `example.py` with the following content:

```python
# This is a simple Python script
def greet(name):
    """This function greets the user."""
    message = f"Hello, {name}! Welcome to SpiceCode."
    print(message)

if __name__ == "__main__":
    # Get user input
    user_name = input("Enter your name: ") # Inline comment
    greet(user_name)
```

Now, navigate your terminal to the directory containing `example.py` and run the basic analysis command:

```bash
spice analyze example.py
```

Upon executing this command, SpiceCode will parse the `example.py` file using its native Python lexer and parser. It will then present you with an interactive menu, listing the various analysis metrics available for this file type. This menu allows you to select specific analyses you are interested in, offering a targeted approach to understanding your code.

## Running All Analyses

If you prefer to run all available analyses for a file without the interactive menu, you can use the `--all` flag. This is akin to a Fremen performing a comprehensive scan of their surroundings.

```bash
spice analyze example.py --all
```

This command will execute every applicable analyzer on `example.py` and output the results directly to your terminal. The output will typically include metrics such as line counts (total, code, comments), function complexity, comment ratio, indentation analysis, and more, depending on the language and the specific analyzers implemented.

## Exporting Analysis Results

Often, you'll want to save the analysis results for later review, documentation, or integration into other processes. SpiceCode provides the `export` command for this purpose, allowing you to preserve the valuable insights gathered, much like Fremen carefully store water.

To export the full analysis results of `example.py` to a Markdown file named `analysis_report.md`, you would run:

```bash
spice export example.py --format markdown --output analysis_report.md
```

This command performs all analyses (similar to `analyze --all`) and then writes the formatted results to the specified output file. Besides Markdown (`markdown`), you can export results to JSON (`json`), CSV (`csv`), and HTML (`html`) formats by changing the `--format` argument accordingly. For example, to get a JSON output:

```bash
spice export example.py --format json --output analysis_results.json
```

This JSON output is particularly useful for programmatic consumption of the analysis data.

## Exploring Further

This quick start guide has introduced you to the fundamental operations of SpiceCode: verifying installation, running basic and comprehensive analyses, and exporting the results. You have now taken your first successful steps into the world of SpiceCode analysis.

The subsequent sections of this documentation delve deeper into the various commands, options, specific analyzers, supported languages, and the underlying architecture of the tool. Continue your exploration to fully harness the power of SpiceCode, mastering its capabilities just as Paul Atreides learned to master the ways of the desert and the power of the spice.
