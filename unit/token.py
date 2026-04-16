class _Token:
    """
    词法单元抽象类

    属性:
        token_name: 词法单元名称（默认类名）
        token_str: 词法单元外显值
        token_value: 词法单元值, 若为 None 表示"不重要"

    """
    def __init__(self, token_str: str, token_value: object, token_name: str = "") -> None:
        self.token_name = token_name if len(token_name) <= 0 else str(self.__class__.__name__)
        self.token_str: str = token_str
        self.token_value: object = token_value

    def __repr__(self) -> str:
        return f"<{str(self.__class__.__name__)}: '{self.token_str}'>"


class FuncEml(_Token):
    """
    核心函数 Exp Minus Ln 词元, 特指不可被重新赋值
    """
    def __init__(self) -> None:
        super().__init__("eml", None)


class OpenParen(_Token):
    """
    左圆括号词元
    """
    def __init__(self) -> None:
        super().__init__("(", None)


class CloseParen(_Token):
    """
    右圆括号词元
    """
    def __init__(self) -> None:
        super().__init__(")", None)


class Comma(_Token):
    """
    逗号词元
    """
    def __init__(self) -> None:
        super().__init__(",", None)


class ConstInt(_Token):
    """
    整型常量词元
    """
    def __init__(self, token_value: int) -> None:
        super().__init__(str(token_value), token_value)


class EndOfStmt(_Token):
    """
    语句结束词元
    """
    def __init__(self) -> None:
        super().__init__(";", None)


class IdentVariable(_Token):
    """
    标识变量（函数名或变量名）
    """
    def __init__(self, token_value: str) -> None:
        super().__init__(token_value, token_value)
