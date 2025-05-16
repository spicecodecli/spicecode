from collections import Counter

def detect_indentation(file_path):
    """
    Analyze the indentation type (spaces, tabs, or mixed) and size in a file.
    Returns a dict: {"indentation_type": "spaces"|"tabs"|"mixed"|"unknown", "indentation_size": int}
    """
    indent_types = []
    indent_sizes = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue  # skip empty lines
            leading_ws = line[:len(line) - len(line.lstrip())]
            if not leading_ws:
                continue
            if set(leading_ws) == {" "}:
                indent_types.append("spaces")
                indent_sizes.append(len(leading_ws))
            elif set(leading_ws) == {"\t"}:
                indent_types.append("tabs")
                indent_sizes.append(len(leading_ws))
            else:
                indent_types.append("mixed")
                indent_sizes.append(len(leading_ws))

    if not indent_types:
        return {"indentation_type": "unknown", "indentation_size": 0}

    type_counter = Counter(indent_types)
    if "spaces" in type_counter or "tabs" in type_counter:
        main_type = "spaces" if type_counter["spaces"] >= type_counter["tabs"] else "tabs"
    else:
        main_type = "mixed"

    size_counter = Counter(
        size for t, size in zip(indent_types, indent_sizes) if t == main_type
    )
    main_size = size_counter.most_common(1)[0][0] if size_counter else 0

    return {"indentation_type": main_type, "indentation_size": main_size}