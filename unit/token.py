from typing import Optional


def calculate_lineno_and_offset(
        text: str, lineno: Optional[int], offset: Optional[int]
) -> tuple[Optional[int], Optional[int]]:
    if lineno is None and offset is None:
        return None, None
    elif lineno is not None and offset is not None:
        new_line_count = text.count("\n")
        new_line_rfind = text.rfind("\n")

        next_lineno = lineno + new_line_count
        next_offset = (
            (offset + len(text)) if new_line_rfind < 0 else (len(text) - new_line_rfind)
        )
        return next_lineno, next_offset
    else:
        assert False


class Token:
    """
    词法单元抽象类

    属性:
        token_name: 词法单元名称（默认类名）
        token_str: 词法单元外显值
        token_value: 词法单元值, 若为 None 表示"不重要"

    """

    def __init__(
            self, token_str: str, token_value: object, token_name: str = "", **kwargs
    ) -> None:
        self.token_name = (
            token_name if len(token_name) <= 0 else str(self.__class__.__name__)
        )
        self.token_str: str = token_str
        self.token_value: object = token_value

        file_name = kwargs["file_name"] if "file_name" in kwargs.keys() else None
        lineno = kwargs["lineno"] if "lineno" in kwargs.keys() else None
        offset = kwargs["offset"] if "offset" in kwargs.keys() else None
        text = kwargs["text"] if "text" in kwargs.keys() else None

        if lineno is None and offset is None:
            pass
        elif lineno is not None and offset is not None:
            assert isinstance(lineno, int) and isinstance(offset, int)
        else:
            assert False

        end_lineno, end_offset = calculate_lineno_and_offset(token_str, lineno, offset)

        self.info: tuple[
            Optional[str],
            Optional[int],
            Optional[int],
            Optional[str],
            Optional[int],
            Optional[int],
        ] = (file_name, lineno, offset, text, end_lineno, end_offset)

    def __repr__(self) -> str:
        return f"<{str(self.__class__.__name__)}: '{self.token_str}'>"


class FuncEml(Token):
    """
    核心函数 Exp Minus Ln 词元, 特指不可被重新赋值
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("eml", None, **kwargs)


class OpenParen(Token):
    """
    左圆括号词元
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("(", None, **kwargs)


class CloseParen(Token):
    """
    右圆括号词元
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(")", None, **kwargs)


class Comma(Token):
    """
    逗号词元
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(",", None, **kwargs)


class ConstInt(Token):
    """
    整型常量词元
    """

    def __init__(self, token_value: int, **kwargs) -> None:
        super().__init__(str(token_value), token_value, **kwargs)


class EndOfStmt(Token):
    """
    语句结束词元
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(";", None, **kwargs)


class IdentVariable(Token):
    """
    标识变量（函数名或变量名）词元
    """

    def __init__(self, token_value: str, **kwargs) -> None:
        super().__init__(token_value, token_value, **kwargs)


class WhiteSpace(Token):
    """
    空白字符（制表符，空格等）
    """

    def __init__(self, token_value: str, **kwargs) -> None:
        super().__init__(
            token_value.encode("unicode_escape").decode("ascii"), token_value, **kwargs
        )


class Assignment(Token):
    """
    赋值词元
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("=", None, **kwargs)


class Annotation(Token):
    """注释词元"""

    def __init__(self, token_value: str, **kwargs) -> None:
        super().__init__(
            token_value.encode("unicode_escape").decode("ascii"), token_value, **kwargs
        )


class Unknown(Token):
    """
    未知词元
    """

    def __init__(self, token_value: str, **kwargs) -> None:
        super().__init__(
            token_value.encode("unicode_escape").decode("ascii"), token_value, **kwargs
        )


class ParameterVariable(IdentVariable):
    """
    变量（特指函数参数，AST 专用）词元
    """

    def __init__(self, ident_variable: IdentVariable):
        assert isinstance(ident_variable.token_value, str)
        info = ident_variable.info[:4]
        super().__init__(ident_variable.token_value, file_name=info[0], lineno=info[1], offset=info[2], text=info[3])


class FunctionVariable(IdentVariable):
    """
    变量（特指函数参数，AST 专用）词元
    """

    def __init__(self, ident_variable: IdentVariable):
        assert isinstance(ident_variable.token_value, str)
        info = ident_variable.info[:4]
        super().__init__(ident_variable.token_value, file_name=info[0], lineno=info[1], offset=info[2], text=info[3])
