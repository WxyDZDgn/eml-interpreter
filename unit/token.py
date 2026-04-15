"""from enum import Enum, auto, unique


@unique
class TokenType(Enum):
    F_EML = auto() # function, exp minus ln, build-in function
    L_PAREN = auto() # left, or open, parenthesis
    R_PAREN = auto() # right, or close, parenthesis
    COMMA = auto() # comma, function arguments delimiter
    C_INT = auto() # constant int"""

"""_expected_value_type_for_token_type_dict = {
    TokenType.F_EML: object,
    TokenType.L_PAREN: object,
    TokenType.R_PAREN: object,
    TokenType.COMMA: object,
    TokenType.C_INT: int
}"""


class _Token:
    """
    词法单元抽象类

    属性:
        token_name: 词法单元名称
        token_str: 词法单元外显值
        token_value: 词法单元值, 若为 None 表示"不重要"

    """
    def __init__(self, token_name: str, token_str: str, token_value: object) -> None:
        self.token_name: str = token_name
        self.token_str: str = token_str
        self.token_value: object = token_value

    def __repr__(self) -> str:
        return f'<{self.token_name}: {self.token_str}>'


class FuncEml(_Token):
    def __init__(self) -> None:
        super().__init__("FuncEml", "eml", None)


class OpenParen(_Token):
    def __init__(self) -> None:
        super().__init__("OpenParen", "(", None)


class CloseParen(_Token):
    def __init__(self) -> None:
        super().__init__("CloseParen", ")", None)


class Comma(_Token):
    def __init__(self) -> None:
        super().__init__("Comma", ",", None)


class ConstInt(_Token):
    def __init__(self, token_value: int) -> None:
        super().__init__("ConstInt", str(token_value), token_value)
