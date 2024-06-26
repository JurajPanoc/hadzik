from dataclasses import dataclass
import hdztokentypes as tt
from hdzerrors import ErrorHandler


@dataclass(slots=True)
class Token:
    type: str
    value: str | None = None


def is_valid_keyword_content(char: str) -> bool:
    """
    used for checking the remaining character in an identifier / keyword
    """
    return char.isalpha() or char.isdigit() or char == "_"


def search_for_keyword(potential_keyword: str) -> Token:
    """
    sees if a keyword is in the tokens list, otherwise makes an identifier
    """
    if potential_keyword in tt.all_token_types:
        return Token(type=potential_keyword, value=None)
    else:
        return Token(type=tt.identifier, value=potential_keyword)


class Tokenizer(ErrorHandler):
    def __init__(self, file_content: str) -> None:
        super().__init__(file_content)
        self.current_char: str | None = None
        self.index: int = -1
        self.advance()
    
    def advance(self):
        self.index += 1
        self.column_number += 1
        self.current_char = self.file_content[self.index] if self.index < len(self.file_content) else None

    def look_ahead(self,step: int = 1) -> str | None:
        """
        looks ahead step characters from the current characters
        """
        return self.file_content[self.index + step] if self.index + step < len(self.file_content) else None

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
                while self.current_char.isnumeric():  # or self.current_char == ".":
                    buffer += self.current_char
                    self.advance()
                type_of_number = tt.integer  # if "." not in buffer else tt.floating_number
                tokens.append(Token(type=type_of_number, value=buffer))
                buffer = ""

            elif char == "\n":
                self.advance()
                tokens.append(Token(type=tt.end_line))
                self.line_number += 1
                self.column_number = 1
            elif char == " ":
                self.advance()
            elif char == "(":
                self.advance()
                tokens.append(Token(type=tt.left_paren))
            elif char == ")":
                self.advance()
                tokens.append(Token(type=tt.right_paren))
            elif char == "=":
                self.advance()
                tokens.append(Token(type=tt.equals))
            elif char == "+":
                self.advance()
                tokens.append(Token(type=tt.plus))
            elif char == "-":
                self.advance()
                tokens.append(Token(type=tt.minus))
            elif char == "*":
                self.advance()
                tokens.append(Token(type=tt.star))
            elif char == "/" and self.look_ahead() == "/":
                self.advance()
                while self.current_char != "\n":
                    self.advance()
            elif char == "/":
                self.advance()
                tokens.append(Token(type=tt.slash))
            else:
                self.raise_error("Syntax", "char not included in the lexer")
        return tokens
