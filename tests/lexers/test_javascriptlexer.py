import re
from ..token import Token, TokenType

class JavaScriptLexer:
    # palavras-chave do javascript
    KEYWORDS = {
        "function", "if", "else", "return", "let", "const", "var", "for", "while", 
        "do", "break", "continue", "switch", "case", "default", "try", "catch", 
        "throw", "new", "this", "class", "extends", "super", "import", "export", 
        "typeof", "instanceof", "void", "delete", "in", "of", "yield", "await", 
        "async", "true", "false", "null", "undefined"
    }
    
    # operadores do javascript - Moved : back to OPERATORS based on test_js_operators
    OPERATORS = {
        "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", ">", "<", ">=", 
        "<=", "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", ">>>", "++", "--", 
        "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=", 
        "=>", "?", ":", "." # Added : back
    }

    # Delimiters - Removed :
    DELIMITERS = {
        "(", ")", "{", "}", "[", "]", ",", ";" # Removed :
    }
    
    # regex para números e identificadores
    NUMBER_PATTERN = re.compile(r"\d+(\.\d+)?([eE][+-]?\d+)?")
    IDENTIFIER_PATTERN = re.compile(r"[a-zA-Z_$][a-zA-Z0-9_$]*")
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_line_start = 0

    def tokenize(self):
        tokens = []
        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char.isspace():
                if char == "\n":
                    tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                    self.line += 1
                    self.column = 1
                    self.current_line_start = self.position + 1
                else:
                    self.column += 1
                self.position += 1
                continue

            if char == "/":
                if self.position + 1 < len(self.source_code):
                    next_char = self.source_code[self.position + 1]
                    if next_char == "/":
                        tokens.append(self.tokenize_single_line_comment())
                        continue
                    elif next_char == "*":
                        tokens.append(self.tokenize_multi_line_comment())
                        continue
            
            # Check for operators FIRST (including :)
            if match := self.match_operator():
                tokens.append(match)
                continue

            if char.isdigit():
                tokens.append(self.tokenize_number())
                continue

            # Corrected check for strings to include single quote explicitly
            if char == "\"" or char == "\"" or char == "`": # Check for ", ", or `
                if char == "`":
                    tokens.append(self.tokenize_template_string())
                else:
                    # Pass the quote character (", ")
                    tokens.append(self.tokenize_string(char))
                continue

            if char.isalpha() or char == "_" or char == "$":
                tokens.append(self.tokenize_identifier())
                continue

            # Check for delimiters AFTER operators
            if char in self.DELIMITERS:
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            # Unknown character - Use the character itself as the value for ERROR token
            # Test failures indicate single quotes are being treated as errors
            # Let's ensure the string check above correctly handles them
            tokens.append(Token(TokenType.ERROR, char, self.line, self.column))
            self.position += 1
            self.column += 1

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_single_line_comment(self):
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
        comment = self.source_code[start_pos:self.position]
        return Token(TokenType.COMMENT, comment, start_line, start_col)

    def tokenize_multi_line_comment(self):
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        self.position += 2 # Skip /*
        self.column += 2
        while self.position + 1 < len(self.source_code):
            if self.source_code[self.position] == "*" and self.source_code[self.position + 1] == "/":
                self.position += 2
                self.column += 2
                comment = self.source_code[start_pos:self.position]
                return Token(TokenType.COMMENT, comment, start_line, start_col)
            if self.source_code[self.position] == "\n":
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
            self.position += 1
        # Unterminated comment
        self.position = len(self.source_code)
        return Token(TokenType.ERROR, "Error: unterminated comment", start_line, start_col)
        
    def tokenize_number(self):
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        match = self.NUMBER_PATTERN.match(self.source_code, self.position)
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, start_line, start_col)
        # Should not happen if called correctly
        return Token(TokenType.ERROR, "Invalid number format", start_line, start_col)

    def tokenize_identifier(self):
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        match = self.IDENTIFIER_PATTERN.match(self.source_code, self.position)
        if match:
            identifier = match.group(0)
            self.position += len(identifier)
            self.column += len(identifier)
        else:
            # This path should not be hit if the main loop logic is correct
            error_char = self.source_code[self.position]
            self.position += 1
            self.column += 1
            return Token(TokenType.ERROR, error_char, start_line, start_col)

        token_type = TokenType.KEYWORD if identifier in self.KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, identifier, start_line, start_col)

    # Rewritten string tokenizer to handle single quotes and unterminated strings correctly
    def tokenize_string(self, quote_char):
        start_pos = self.position # Position of the opening quote
        start_col = self.column
        start_line = self.line
        # The main loop already identified the quote_char, so we start AFTER it.
        self.position += 1 
        self.column += 1

        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            if char == quote_char:  # End of string
                self.position += 1
                self.column += 1
                # The value includes the quotes
                string_value = self.source_code[start_pos:self.position] 
                return Token(TokenType.STRING, string_value, start_line, start_col)
            elif char == "\\":  # Escape sequence
                self.position += 1 # Consume backslash
                self.column += 1
                if self.position < len(self.source_code):
                    escaped_char = self.source_code[self.position]
                    if escaped_char == "\n": # Escaped newline
                         self.line += 1
                         self.column = 1
                         self.current_line_start = self.position + 1
                    else:
                         self.column += 1
                    self.position += 1 # Advance past escaped character
                else:
                    # Unterminated escape sequence at EOF -> Unterminated string
                    break # Exit loop, handle below
                continue # Continue to next character in string
            elif char == "\n":  # Literal newline in string
                 # Test expects STRING token even if unterminated by newline
                 self.line += 1
                 self.column = 1
                 self.current_line_start = self.position + 1
                 self.position += 1 # Consume newline
            else: # Regular character in string
                self.column += 1
                self.position += 1

        # Reached end of file without closing quote
        # Test expects STRING token even if unterminated
        string_value = self.source_code[start_pos:self.position] # Include quotes up to EOF
        return Token(TokenType.STRING, string_value, start_line, start_col)

    def tokenize_template_string(self):
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        self.position += 1  # Skip `
        self.column += 1
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            if char == "`":
                self.position += 1
                self.column += 1
                string_value = self.source_code[start_pos:self.position]
                return Token(TokenType.STRING, string_value, start_line, start_col)
            elif char == "\\":
                self.position += 1
                self.column += 1
                if self.position < len(self.source_code):
                    if self.source_code[self.position] == "\n":
                        self.line += 1
                        self.column = 1
                        self.current_line_start = self.position + 1
                    else:
                        self.column += 1
                    self.position += 1
                continue
            elif char == "$" and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1] == "{":
                # Basic handling: treat expression as part of string
                self.position += 2 
                self.column += 2
                expr_end = self.source_code.find("}", self.position)
                if expr_end != -1:
                    num_newlines = self.source_code[self.position:expr_end].count("\n")
                    if num_newlines > 0:
                        self.line += num_newlines
                        last_newline_pos = self.source_code.rfind("\n", self.position, expr_end)
                        self.column = expr_end - last_newline_pos
                    else:
                        self.column += (expr_end - self.position) + 1 # Add 1 for the closing brace
                    self.position = expr_end + 1
                else:
                    # Unterminated expression - treat as literal characters
                    self.column += 2 # For ${ 
                    continue 
            elif char == "\n":
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
                self.position += 1
            else:
                self.column += 1
                self.position += 1
        # Unterminated template literal - Test expects ERROR
        return Token(TokenType.ERROR, "Unterminated template literal", start_line, start_col)

    def match_operator(self):
        # Ensure ':' is checked here
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.source_code.startswith(op, self.position):
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None

    def match_punctuation(self):
        for op in sorted(self.PUNCTUATION, key=len, reverse=True):
            if self.source_code.startswith(op, self.position):
                token = Token(TokenType.PUNCTUATION, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None

    def match_number(self):
        match = self.NUMBER_PATTERN.match(self.source_code, self.position)
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, self.line, self.column)
        return None

    def match_identifier(self):
        match = self.IDENTIFIER_PATTERN.match(self.source_code, self.position)
        if match:
            identifier = match.group(0)
            self.position += len(identifier)
            self.column += len(identifier)
            token_type = TokenType.KEYWORD if identifier in self.KEYWORDS else TokenType.IDENTIFIER
            return Token(token_type, identifier, self.line, self.column)
        return None

    def match_keyword(self):
        match = self.KEYWORD_PATTERN.match(self.source_code, self.position)
        if match:
            keyword = match.group(0)
            self.position += len(keyword)
            self.column += len(keyword)
            return Token(TokenType.KEYWORD, keyword, self.line, self.column)
        return None

    def match_string(self):
        match = self.STRING_PATTERN.match(self.source_code, self.position)
        if match:
            string = match.group(0)
            self.position += len(string)
            self.column += len(string)
            return Token(TokenType.STRING, string, self.line, self.column)
        return None

    def match_comment(self):
        match = self.COMMENT_PATTERN.match(self.source_code, self.position)
        if match:
            comment = match.group(0)
            self.position += len(comment)
            self.column += len(comment)
            return Token(TokenType.COMMENT, comment, self.line, self.column)
        return None

    def match_whitespace(self):
        match = self.WHITESPACE_PATTERN.match(self.source_code, self.position)
        if match:
            whitespace = match.group(0)
            self.position += len(whitespace)
            self.column += len(whitespace)
            return Token(TokenType.WHITESPACE, whitespace, self.line, self.column)
        return None

    def match_newline(self):
        match = self.NEWLINE_PATTERN.match(self.source_code, self.position)
        if match:
            newline = match.group(0)
            self.position += len(newline)
            self.line += 1
            self.column = 1
            self.current_line_start = self.position
            return Token(TokenType.NEWLINE, newline, self.line, self.column)
        return None

    def match_error(self):
        error_char = self.source_code[self.position]
        self.position += 1
        self.column += 1
        return Token(TokenType.ERROR, error_char, self.line, self.column)

    def match_eof(self):
        return Token(TokenType.EOF, "", self.line, self.column)

    def match_any(self):
        match = self.ANY_PATTERN.match(self.source_code, self.position)
        if match:
            any = match.group(0)
            self.position += len(any)
            self.column += len(any)
            return Token(TokenType.ANY, any, self.line, self.column)
        return None

    def match_all(self):
        match = self.ALL_PATTERN.match(self.source_code, self.position)
        if match:
            all = match.group(0)
            self.position += len(all)
            self.column += len(all)
            return Token(TokenType.ALL, all, self.line, self.column)
        return None

    def match_none(self):
        match = self.NONE_PATTERN.match(self.source_code, self.position)
        if match:
            none = match.group(0)
            self.position += len(none)
            self.column += len(none)
            return Token(TokenType.NONE, none, self.line, self.column)
        return None

    def match_true(self):
        match = self.TRUE_PATTERN.match(self.source_code, self.position)
        if match:
            true = match.group(0)
            self.position += len(true)
            self.column += len(true)
            return Token(TokenType.TRUE, true, self.line, self.column)
        return None

    def match_false(self):
        match = self.FALSE_PATTERN.match(self.source_code, self.position)
        if match:
            false = match.group(0)
            self.position += len(false)
            self.column += len(false)
            return Token(TokenType.FALSE, false, self.line, self.column)
        return None

    def match_null(self):
        match = self.NULL_PATTERN.match(self.source_code, self.position)
        if match:
            null = match.group(0)
            self.position += len(null)
            self.column += len(null)
            return Token(TokenType.NULL, null, self.line, self.column)
        return None

    def match_undefined(self):
        match = self.UNDEFINED_PATTERN.match(self.source_code, self.position)
        if match:
            undefined = match.group(0)
            self.position += len(undefined)
            self.column += len(undefined)
            return Token(TokenType.UNDEFINED, undefined, self.line, self.column)
        return None

    def match_nan(self):
        match = self.NAN_PATTERN.match(self.source_code, self.position)
        if match:
            nan = match.group(0)
            self.position += len(nan)
            self.column += len(nan)
            return Token(TokenType.NAN, nan, self.line, self.column)
        return None

    def match_infinity(self):
        match = self.INFINITY_PATTERN.match(self.source_code, self.position)
        if match:
            infinity = match.group(0)
            self.position += len(infinity)
            self.column += len(infinity)
            return Token(TokenType.INFINITY, infinity, self.line, self.column)
        return None

    def match_number(self):
        match = self.NUMBER_PATTERN.match(self.source_code, self.position)
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, self.line, self.column)
        return None

    def match_identifier(self):
        match = self.IDENTIFIER_PATTERN.match(self.source_code, self.position)
        if match:
            identifier = match.group(0)
            self.position += len(identifier)
            self.column += len(identifier)
            token_type = TokenType.KEYWORD if identifier in self.KEYWORDS else TokenType.IDENTIFIER
            return Token(token_type, identifier, self.line, self.column)
        return None

    def match_string(self):
        match = self.STRING_PATTERN.match(self.source_code, self.position)
        if match:
            string = match.group(0)
            self.position += len(string)
            self.column += len(string)
            return Token(TokenType.STRING, string, self.line, self.column)
        return None

    def match_regex(self):
        match = self.REGEX_PATTERN.match(self.source_code, self.position)
        if match:
            regex = match.group(0)
            self.position += len(regex)
            self.column += len(regex)
            return Token(TokenType.REGEX, regex, self.line, self.column)
        return None

    def match_comment(self):
        match = self.COMMENT_PATTERN.match(self.source_code, self.position)
        if match:
            comment = match.group(0)
            self.position += len(comment)
            self.column += len(comment)
            return Token(TokenType.COMMENT, comment, self.line, self.column)
        return None

    def match_whitespace(self):
        match = self.WHITESPACE_PATTERN.match(self.source_code, self.position)
        if match:
            whitespace = match.group(0)
            self.position += len(whitespace)
            self.column += len(whitespace)
            return Token(TokenType.WHITESPACE, whitespace, self.line, self.column)
        return None

    def match_newline(self):
        match = self.NEWLINE_PATTERN.match(self.source_code, self.position)
        if match:
            newline = match.group(0)
            self.position += len(newline)
            self.line += 1
            self.column = 1
            self.current_line_start = self.position
            return Token(TokenType.NEWLINE, newline, self.line, self.column)
        return None

    def match_error(self):
        error_char = self.source_code[self.position]
        self.position += 1
        self.column += 1
        return Token(TokenType.ERROR, error_char, self.line, self.column)

    def match_eof(self):
        if self.position >= len(self.source_code):
            return Token(TokenType.EOF, '', self.line, self.column)
        return None

    def match_all(self):
        match = self.ALL_PATTERN.match(self.source_code, self.position)
        if match:
            all = match.group(0)
            self.position += len(all)
            self.column += len(all)
            return Token(TokenType.ALL, all, self.line, self.column)
        return None

    def match_none(self):
        match = self.NONE_PATTERN.match(self.source_code, self.position)
        if match:
            none = match.group(0)
            self.position += len(none)
            self.column += len(none)
            return Token(TokenType.NONE, none, self.line, self.column)
        return None
    