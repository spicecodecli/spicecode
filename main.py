# main.py

from lexers.ruby.rubylexer import RubyLexer
from parser.parser import Parser


if __name__ == "__main__":
    # Sample Ruby code
    code = """
    def hello
      puts "Hello, world!"
      result = 42 + 3
      is_valid = true
      my_symbol = :ruby
    end
    """
    
    lexer = RubyLexer(code)
    tokens = lexer.tokenize()

    print("Tokens:")
    for token in tokens:
        print(token)
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAST:")
    print(ast)
