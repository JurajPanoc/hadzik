from dataclasses import dataclass
import token_types as tt
from hdzerrors import raise_error


@dataclass(slots=True)
class Token:
    type: str
    value: str | None = None


def is_valid_keyword_content(char: str) -> bool:
    return char.isalpha() or char.isdigit() or char == "_"


def search_for_keyword(potential_keyword: str) -> Token:
    if potential_keyword != tt.identifier and potential_keyword in tt.all_token_types:
        return Token(type=potential_keyword, value=None)
    else:
        return Token(type=tt.identifier, value=potential_keyword)


class Tokenizer:
    def __init__(self, file_content: str) -> None:
        self.file_content = file_content
        self.current_char: str | None = None
        self.index: int = -1
        self.line_index: int = 1
        self.column_index: int = 0
        self.advance()
    
    def advance(self):
        self.index += 1
        self.column_index = self.index
        self.current_char = self.file_content[self.index] if self.index < len(self.file_content) else None

    def tokenize(self):
        tokens: list[Token] = []
        while self.current_char is not None:
            char: str = self.current_char
            buffer = ""

            if char.isalpha() or char == "_": #makes keywords, if not a keyword makes an identifier
                buffer += char
                self.advance()
                while is_valid_keyword_content(self.current_char):
                    buffer += self.current_char
                    self.advance()
                tokens.append(search_for_keyword(buffer))
                buffer = ""
            
            elif char.isnumeric(): #makes numbers, ints only for now
                buffer += char
                self.advance()
                while self.current_char.isnumeric() or self.current_char == ".":
                    buffer += self.current_char
                    self.advance()
                type_of_number = tt.integer if "." not in buffer else tt.floating_number
                tokens.append(Token(type=type_of_number, value=buffer))
                buffer = ""

            elif char == "\n":
                tokens.append(Token(type=tt.end_line))
                self.line_index += 1
                self.column_index = 0
                self.advance()
            elif char == " ":
                self.advance()
            elif char == "(":
                tokens.append(Token(type=tt.left_paren))
                self.advance()
            elif char == ")":
                tokens.append(Token(type=tt.right_paren))
                self.advance()
            else:
                raise_error("Syntax", "char not included in the lexer", 
                            self.file_content, self.line_index, self.column_index)
        return tokens