---
sidebar_position: 1
---

# Using the SpiceCode CLI

Interacting with SpiceCode is primarily done through its Command Line Interface (CLI). Designed for ease of use and flexibility, the CLI provides a set of commands to perform code analysis, manage settings, and export results. This guide details the available commands and their options, empowering you to effectively wield SpiceCode like a Fremen masterfully handling their maker hooks to navigate the great sandworms.

## Core Commands

SpiceCode offers several core commands for basic interaction and configuration.

### Checking the Version

To determine the currently installed version of SpiceCode, you can use the `version` command. This is often the first step to ensure the tool is installed correctly and to know which specific release you are working with.

```bash
spice version
```

Executing this command will display the version number, such as `SpiceCode version 1.0.0`.

### Displaying a Welcome Message

For a simple confirmation that the CLI is responsive, or just for a friendly greeting reminiscent of Fremen hospitality, you can use the `hello` command.

```bash
spice hello
```

This command outputs a standard welcome message from the SpiceCode tool.

### Configuring Language Settings

SpiceCode supports multiple interface languages, allowing users to interact with the tool in their preferred language, much like the diverse dialects spoken across the sietches of Arrakis. The `translate` command initiates an interactive prompt to select and set the desired language for CLI output and messages.

```bash
spice translate
```

Follow the on-screen prompts to choose from the available language options.

## Code Analysis Commands

The heart of SpiceCode lies in its ability to analyze source code. The `analyze` command is the gateway to these capabilities.

### Basic Interactive Analysis

To initiate an analysis on a specific source code file, use the `analyze` command followed by the path to the file.

```bash
spice analyze path/to/your/codefile.ext
```

Replace `path/to/your/codefile.ext` with the actual path to the file you wish to analyze (e.g., `src/main.py`, `lib/utils.js`). When run in this basic form, SpiceCode first identifies the programming language based on the file extension. It then parses the code and presents an interactive menu listing all the analysis metrics applicable to that language. You can navigate this menu using your keyboard to select one or more specific analyses to perform. The results of the selected analyses are then displayed directly in the terminal.

### Comprehensive Analysis (`--all`)

If you wish to perform all available analyses for a given file without the need for interactive selection, you can append the `--all` flag to the `analyze` command. This provides a complete overview of the file's metrics in one go, similar to a Fremen conducting a thorough reconnaissance.

```bash
spice analyze path/to/your/codefile.ext --all
```

This command runs every analyzer relevant to the detected language and prints a consolidated report of all results to the terminal.

### JSON Output (`--json`)

For scenarios where you need to programmatically process the analysis results, such as integrating SpiceCode into automated workflows or other tools, you can request the output in JSON format using the `--json` flag.

```bash
spice analyze path/to/your/codefile.ext --json
```

This command performs the analysis (either interactively or with `--all` if combined) and outputs the results as a structured JSON object to the standard output. This format is ideal for parsing and further processing by scripts or applications.

```bash
# Example combining --all and --json
spice analyze path/to/your/codefile.ext --all --json
```

## Exporting Analysis Results

While the `analyze` command is useful for immediate feedback, the `export` command allows you to save comprehensive analysis results to files in various formats. This is essential for record-keeping, report generation, or sharing findings, akin to Fremen meticulously documenting their water discipline.

The `export` command requires the path to the source file and typically involves specifying the desired output format and the path for the output file.

```bash
spice export path/to/your/codefile.ext --format <FORMAT> --output <OUTPUT_PATH>
```

-   `path/to/your/codefile.ext`: The source code file to be analyzed.
-   `--format <FORMAT>`: Specifies the desired output format. Supported formats are:
    -   `json`: JavaScript Object Notation
    -   `csv`: Comma-Separated Values
    -   `markdown`: Markdown text format
    -   `html`: HTML document format
-   `--output <OUTPUT_PATH>`: Specifies the file path where the results should be saved.

**Examples:**

Exporting analysis results to a Markdown file:
```bash
spice export src/app.go --format markdown --output reports/app_analysis.md
```

Exporting analysis results to a JSON file:
```bash
spice export lib/parser.rb --format json --output data/parser_metrics.json
```

Exporting analysis results to a CSV file:
```bash
spice export main.py --format csv --output results/main_stats.csv
```

Exporting analysis results to an HTML file:
```bash
spice export component.js --format html --output docs/component_report.html
```

The `export` command implicitly runs all applicable analyses on the specified file before generating the output in the chosen format.

Mastering these CLI commands provides you with the fundamental skills to effectively utilize SpiceCode for understanding and improving your codebase. Explore these commands with your own projects to become as adept with SpiceCode as a Fremen is with the ways of the desert.
