import os

def detect_language(file_path):
    _, ext = os.path.splitext(file_path)

    if ext == ".rb":
        return "ruby"
    elif ext == ".py":
        return "python"
    elif ext == ".js":
        return "javascript"
    elif ext == ".go":
        return "go"
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

# Example usage:
if __name__ == "__main__":
    for path in ["example.py", "example.js", "example.rb", "example.go"]:
        print(f"{path}: {detect_language(path)}")
