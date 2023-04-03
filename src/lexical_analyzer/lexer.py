import re

from src.lexical_errors.error import LexicalError, ErrorTypes
from token_types import TOKEN_TYPES_REGEX, TokenTypes
from tokens import Token

_current_file_name = ""
_string_token = None

_left_brace_count = 0
_right_brace_count = 0


def _token_types_count(tokens: list, token_type: TokenTypes):
    token_type_count = 0
    for token in tokens:
        if token.type == token_type:
            token_type_count += 1
    return token_type_count


def _lex_line(source_code_line: str, line_number: int):

    global _string_token
    global _left_brace_count
    global _right_brace_count

    open_bracket = 0
    open_par = 0
    column_number_error = 0

    if _string_token:
        _string_token.value += "\n"

    line = source_code_line
    column_number = 0
    tokens = []

    regex = TOKEN_TYPES_REGEX[TokenTypes.LEFT_BRACE]
    match_res = re.search(regex, line)
    if match_res:
        _left_brace_count += 1

    regex = TOKEN_TYPES_REGEX[TokenTypes.RIGHT_BRACE]
    match_res = re.search(regex, line)
    if match_res:
        _right_brace_count += 1
        if _right_brace_count > _left_brace_count:
            raise LexicalError(line_number, match_res.start(), ErrorTypes.EXTRA_BRACE)

    while len(line) > 0:
        if _string_token:
            regex = TOKEN_TYPES_REGEX[TokenTypes.DOUBLE_QUOTE]
            match_res = re.search(regex, line)
            # matched
            if match_res and match_res.start() == 0:
                tokens.append(_string_token)
                line = line[match_res.end():]
                _string_token = None
            else:
                _string_token.value += line[0]
                line = line[1:]
            continue

        for token_type, regex in TOKEN_TYPES_REGEX.items():

            match_res = re.search(regex, line)
            if match_res and match_res.start() == 0:

                start = match_res.start()
                end = match_res.end()

                token_value = line[start: end]
                line = line[end:]

                if token_type == TokenTypes.LEFT_BRACKET:
                    if open_bracket == 0:
                        column_number_error = column_number
                    open_bracket += 1

                if token_type == TokenTypes.RIGHT_BRACKET:
                    open_bracket -= 1
                    if open_bracket < 0:
                        raise LexicalError(line_number, column_number + end, ErrorTypes.UNEXPECTED_SYMBOL)

                if token_type == TokenTypes.LEFT_PAR:
                    if open_par == 0:
                        column_number_error = column_number
                    open_par += 1

                if token_type == TokenTypes.RIGHT_PAR:
                    open_par -= 1
                    if open_par < 0:
                        raise LexicalError(line_number, column_number + end, ErrorTypes.UNEXPECTED_SYMBOL)

                if token_type == TokenTypes.DOUBLE_QUOTE:
                    if not _string_token:
                        _string_token = Token(TokenTypes.STRING, "")
                        _string_token.line_pos = line_number
                        _string_token.column_pos = column_number
                        break

                token = Token(token_type, token_value)
                tokens.append(token)
                column_number += end

                # if comment
                if token_type == TokenTypes.LINE_COMMENT:
                    token.value += line
                    return tokens

                break

    if open_bracket > 0:
        raise LexicalError(line_number, column_number_error + 1, ErrorTypes.UNCLOSED_BRACKET)

    if open_par > 0:
        raise LexicalError(line_number, column_number_error + 1, ErrorTypes.UNCLOSED_PAR)

    return tokens


def tokenize_source(filename: str):

    global _current_file_name
    _current_file_name = filename

    lines_count = 1
    tokens = []

    with open(filename, "r") as file:
        for line in file:
            tokens += _lex_line(line.strip(), lines_count)
            lines_count += 1

    if _string_token is not None:
        raise LexicalError(_string_token.line_pos, _string_token.column_pos, ErrorTypes.UNCLOSED_DOUBLE_QUOTES)

    left_brace_count = _token_types_count(tokens, TokenTypes.LEFT_BRACE)
    right_brace_count = _token_types_count(tokens, TokenTypes.RIGHT_BRACE)
    if left_brace_count != right_brace_count:
        diff = left_brace_count - right_brace_count
        if diff > 0:
            line_number = 0
            with open(filename, "r") as file:
                for line in file:
                    line_number += 1
                    regex = TOKEN_TYPES_REGEX[TokenTypes.LEFT_BRACE]
                    match_res = re.search(regex, line)
                    if match_res:
                        column = match_res.start()
                        raise LexicalError(line_number, column,
                                           ErrorTypes.UNCLOSED_BRACE)

    tokens.append(Token(
        TokenTypes.EOF, ""
    ))

    return tokens


print(tokenize_source("input.txt"))
