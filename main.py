import sys
from lexers.ruby.rubylexer import RubyLexer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return
    
    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Run the lexer
    lexer = RubyLexer(source_code)
    tokens = lexer.tokenize()

    print("\nTokens:")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
