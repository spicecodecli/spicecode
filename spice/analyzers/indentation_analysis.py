from collections import Counter

def detect_indentation(file_path):
    """
    Analyze the indentation type (spaces or tabs) and size in a file.
    Returns a dict: {"indentation_type": "spaces" or "tabs" or "mixed" or "unknown", "indentation_size": int}
    """
    indent_types = []
    indent_sizes = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.lstrip()
            if not stripped or line == stripped:
                continue  # skip empty or non-indented lines
            indent = line[:len(line) - len(stripped)]
            if set(indent) == {" "}:
                indent_types.append("spaces")
                indent_sizes.append(len(indent))
            elif set(indent) == {"\t"}:
                indent_types.append("tabs")
                indent_sizes.append(len(indent))
            else:
                indent_types.append("mixed")
                indent_sizes.append(len(indent))

    if not indent_types:
        return {"indentation_type": "unknown", "indentation_size": 0}

    # Find the most common indentation type (excluding 'mixed' if possible, because time)
    type_counter = Counter(indent_types)
    if "spaces" in type_counter or "tabs" in type_counter:
        # Prefer spaces or tabs over mixed
        main_type = "spaces" if type_counter["spaces"] >= type_counter["tabs"] else "tabs"
    else:
        main_type = "mixed"

    # Find the most common indentation size for the main type
    size_counter = Counter(
        size for t, size in zip(indent_types, indent_sizes) if t == main_type
    )
    if size_counter:
        main_size = size_counter.most_common(1)[0][0]
    else:
        main_size = 0

    return {"indentation_type": main_type, "indentation_size": main_size}