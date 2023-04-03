from enum import Enum


class ErrorTypes(Enum):
    UNDEFINED_TOKEN = "undefined token: "
    UNCLOSED_DOUBLE_QUOTES = "unclosed double quotes: "
    UNCLOSED_BRACKET = "unclosed bracket: "
    UNCLOSED_BRACE = "unclosed brace: "
    EXTRA_BRACE = "extra brace: "
    UNCLOSED_PAR = "unclosed par: "
    UNEXPECTED_SYMBOL = "unexpected symbol: "


class LexicalError(Exception):
    def __init__(self, line, column, type_error):
        self.line = line
        self.column = column
        self.message = f"lexical error occured: \n" \
                       f"{type_error}\n" \
                       f"line: {line}   column: {column}"
        super().__init__(self.message)
