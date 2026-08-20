import re

from src.errors import LexerError


class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (f"Token(" f"{self.type}, " f"{self.value!r}, " f"line={self.line}, " f"column={self.column}" f")")


class Lexer:
    def __init__(self, source, file_name=None):
        self.source = source
        self.file_name = file_name

    def tokenize(self):
        token_patterns = [
            ("COMMENT", r"\#[^\n]*"),
            ("STRING", r'"[^"]*"'),
            ("NUMBER", r"\d+(?:\.\d+)?"),
            ("ARROW", r"->"),
            ("GREATER_EQUAL", r">="),
            ("LESS_EQUAL", r"<="),
            ("EQUAL_EQUAL", r"=="),
            ("NOT_EQUAL", r"!="),
            ("GREATER", r">"),
            ("LESS", r"<"),
            ("PLUS", r"\+"),
            ("MINUS", r"-"),
            ("MULTIPLY", r"\*"),
            ("DIVIDE", r"/"),
            ("MODULO", r"%"),
            ("POWER", r"\^"),
            ("EQUALS", r"="),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"\{"),
            ("RBRACE", r"\}"),
            ("LBRACKET", r"\["),
            ("RBRACKET", r"\]"),
            ("COMMA", r","),
            ("COLON", r":"),
            ("IDENTIFIER", r"[A-Za-z_\u0900-\u097F]" r"[A-Za-z0-9_\u0900-\u097F]*"),
            ("WHITESPACE", r"\s+"),
            ("UNKNOWN", r"."),
        ]

        pattern = "|".join(f"(?P<{name}>{regex})" for name, regex in token_patterns)

        keywords = {
            "देखाऊ": "PRINT", "सोध": "INPUT",
            "पूर्णाङ्क": "INTEGER_TYPE", "दशमलव": "FLOAT_TYPE",
            "पाठ": "STRING_TYPE", "सत्य": "BOOLEAN_TYPE",
            "सूची": "LIST_TYPE", "नक्सा": "MAP_TYPE",
            "सही": "TRUE", "गलत": "FALSE",
            "यदि": "IF", "नत्र": "ELSE", "अन्यथा": "ELSE",
            "जब": "WHILE", "हरेक": "FOR_EACH", "मा": "IN",
            "र": "AND", "वा": "OR", "होइन": "NOT",
            "काम": "FUNCTION", "फर्काऊ": "RETURN",
            "रोक": "BREAK", "जारी": "CONTINUE", "प्रयोग": "IMPORT",
        }

        tokens = []
        line = 1
        column = 1

        for match in re.finditer(pattern, self.source, re.UNICODE):
            token_type = match.lastgroup
            value = match.group()
            token_line = line
            token_column = column

            if token_type == "IDENTIFIER":
                token_type = keywords.get(value, "IDENTIFIER")

            if token_type == "UNKNOWN":
                raise LexerError(f"नचिनिएको चिन्ह: {value}", file_name=self.file_name, line=token_line, column=token_column)

            if token_type not in ("WHITESPACE", "COMMENT"):
                tokens.append(Token(token_type, value, token_line, token_column))

            for character in value:
                if character == "\n":
                    line += 1
                    column = 1
                else:
                    column += 1

        return tokens
