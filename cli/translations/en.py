messages = {
    # keys for the hello command
    "welcome": "🌶️   Welcome to [bold red]SpiceCode[/]! 🌶️",
    "description": "🔥 The [yellow]CLI tool[/] that makes your code [yellow]spicier[/] 🥵",
    # error messages
    "error": "Error:",
    "error_file_not_found": "Error: File not found",
    "error_not_a_file": "Error: Not a file",
    "error_reading_file": "Error reading file",
    "error_invalid_format": "Error: Invalid output format",
    "error_unexpected_result": "Error: Unexpected result from analyzer.",
    "error_analyzing_visibility": "Error analyzing visibility",
    # keys for the analyze command output
    "analyzing_file": "Analyzing file",
    "line_count": "The file has {count} lines",
    "function_count": "The file has {count} functions",
    "comment_line_count": "The file has {count} comment lines",
    "inline_comment_count": "The file has {count} inline comments",
    # keys for analyze command checkbox menu
    "select_stats": "Select stats to display:",
    "line_count_option": "Line Count",
    "function_count_option": "Function Count", 
    "comment_line_count_option": "Comment Line Count",
    "inline_comment_count_option": "Inline Comment Count",
    "no_stats_selected": "No stats selected. Analysis cancelled.",
    "confirm_and_analyze": "Confirm and analyze",
    "checkbox_hint": "(Use space to select, enter to confirm)",
    # keys for the version command
    "version_info": "SpiceCode Version:",
    "version_not_found": "Version information not found in setup.py",
    "setup_not_found": "Error: setup.py not found.",

    # General / Reusable
    "file_path_help": "The path to the file to analyze.",
    "output_format_help": "Output format (console, json).",
    "valid_formats_are": "Valid formats are",
    "line_num": "Line No.",
    "content_col": "Content",
    "empty_line": "Empty/Whitespace", # for display in table cell
    "summary_statistics": "Summary Statistics",
    "metric": "Metric",
    "value": "Value",
    "category": "Category",
    "count": "Count",
    "name": "Name",
    "type": "Type", # for function/method type
    "visibility": "Visibility",

    # Indentation Analysis
    "analyze_indentation_help": "Analyzes and reports the indentation levels for each line in the given file.",
    "indentation_analysis_for": "Indentation Analysis for",
    "indentation_details_per_line": "Indentation Details Per Line",
    "indent_level_col": "Indent Level",

    # Dependency Analysis
    "analyze_dependencies_help": "Analyzes and reports the external dependencies for the given file.",
    "dependency_analysis_for": "Dependency Analysis for",
    "dependencies_found": "Dependencies Found",
    "dependency_name": "Dependency Name",
    "no_dependencies_found": "No dependencies found in this file.",

    # Comment/Code Ratio Analysis
    "analyze_comment_code_ratio_help": "Analyzes and reports the comment to code ratio for the given file.",
    "comment_code_ratio_analysis_for": "Comment/Code Ratio Analysis for",
    "total_lines": "Total Lines",
    "code_lines": "Code Lines",
    "comment_lines": "Comment-Only Lines",
    "empty_lines": "Empty/Whitespace Lines",
    "comment_code_ratio": "Comment/Code Ratio",
    "line_by_line_classification": "Line-by-Line Classification",
    "line_type": "Line Type",
    "code": "Code", # as a line type
    "comment_only": "Comment Only", # as a line type
    "empty_or_whitespace": "Empty/Whitespace", # as a line type (key for logic)

    # Visibility Analysis
    "analyze_visibility_help": "Analyzes and reports the visibility of functions and methods (public/private) in the given file.",
    "visibility_analysis_for": "Visibility Analysis for",
    "visibility_summary": "Visibility Summary",
    "public_functions": "Public Functions",
    "private_functions": "Private Functions",
    "public_methods": "Public Methods",
    "private_methods": "Private Methods",
    "details_by_element": "Details by Element",
    "function": "Function", # as a type of element
    "method": "Method", # as a type of element
    "public": "Public", # as visibility status
    "private (convention)": "Private (convention)",
    "private (name mangling)": "Private (name mangling)",
    "no_elements_found_for_visibility": "No functions or methods found for visibility analysis in this file."
}

