def analyze_comment_code_ratio(code_content):
    lines = code_content.splitlines()
    line_details = []
    
    num_code_lines = 0
    num_comment_only_lines = 0
    num_empty_or_whitespace_lines = 0

    for i, line_text in enumerate(lines):
        stripped_line = line_text.strip()
        line_type = ""

        if not stripped_line:
            line_type = "empty_or_whitespace"
            num_empty_or_whitespace_lines += 1
        elif stripped_line.startswith("#"): # Assuming Python style comments
            line_type = "comment_only"
            num_comment_only_lines += 1
        else:
            line_type = "code" # This includes lines with inline comments
            num_code_lines += 1
        
        line_details.append({
            "original_line_number": i + 1,
            "line_content": line_text,
            "stripped_line_content": stripped_line,
            "type": line_type
        })
    
    total_relevant_lines = num_code_lines + num_comment_only_lines
    ratio = 0
    if total_relevant_lines > 0:
        ratio = num_comment_only_lines / total_relevant_lines
    else: 
        ratio = 0

    summary = {
        "total_lines_in_file": len(lines),
        "code_lines": num_code_lines,
        "comment_only_lines": num_comment_only_lines,
        "empty_or_whitespace_lines": num_empty_or_whitespace_lines,
        "comment_to_code_plus_comment_ratio": ratio
    }
    
    return {"line_by_line_analysis": line_details, "summary_stats": summary}

