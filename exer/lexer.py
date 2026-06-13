from unit.token import (
    _Token,
    IdentVariable,
    ConstInt,
    OpenParen,
    CloseParen,
    Comma,
    EndOfStmt,
    WhiteSpace,
    Assignment,
    Annotation,
    _calculate_lineno_and_offset,
)

import re

_text_reg = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
_number_reg = re.compile(r"0|[1-9][0-9]*")
_open_paren_reg = re.compile(r"\(")
_close_paren_reg = re.compile(r"\)")
_comma_reg = re.compile(r",")
_end_of_stmt_reg = re.compile(r";")
_white_space_reg = re.compile(r"[\s\t\n\r]+")
_assignment_reg = re.compile(r"=")
_annotation_inline_reg = re.compile(r"//[^\n]*")
_unknown_reg = re.compile(r"[^0-9a-zA-Z_(),;=/]+")


def lexer(code: str, ignore_annotations_and_whitespaces: bool = True) -> list[_Token]:
    """
    词法分析器

    参数:
        code: 需要转换成词元的代码
        ignore_annotations_and_whittespaces: 返回的词元列表中不包含空白词元和注释词元

    返回:
        list[
            _Token: 代码转词元
        ]: 所有词元的列表
    """
    ls = []
    text_ls: list[str] = code.split("\n")
    pre_idx = 0

    lineno: int = 1
    offset: int = 1

    while pre_idx < len(code):
        cur_str = code[pre_idx:]
        if _ := _text_reg.match(cur_str):
            token_str = _.group()
            ls.append(
                IdentVariable(
                    token_str, lineno=lineno, offset=offset, text=text_ls[lineno - 1]
                )
            )
            pre_idx += _.end()
        elif _ := _number_reg.match(cur_str):
            token_str = _.group()
            ls.append(
                ConstInt(
                    int(token_str),
                    lineno=lineno,
                    offset=offset,
                    text=text_ls[lineno - 1],
                )
            )
            pre_idx += _.end()
        elif _ := _open_paren_reg.match(cur_str):
            token_str = _.group()
            ls.append(OpenParen(lineno=lineno, offset=offset, text=text_ls[lineno - 1]))
            pre_idx += _.end()
        elif _ := _close_paren_reg.match(cur_str):
            token_str = _.group()
            ls.append(
                CloseParen(lineno=lineno, offset=offset, text=text_ls[lineno - 1])
            )
            pre_idx += _.end()
        elif _ := _comma_reg.match(cur_str):
            token_str = _.group()
            ls.append(Comma(lineno=lineno, offset=offset, text=text_ls[lineno - 1]))
            pre_idx += _.end()
        elif _ := _end_of_stmt_reg.match(cur_str):
            token_str = _.group()
            ls.append(EndOfStmt(lineno=lineno, offset=offset, text=text_ls[lineno - 1]))
            pre_idx += _.end()
        elif _ := _white_space_reg.match(cur_str):
            token_str = _.group()
            if not ignore_annotations_and_whitespaces:
                ls.append(
                    WhiteSpace(
                        token_str,
                        lineno=lineno,
                        offset=offset,
                        text=text_ls[lineno - 1],
                    )
                )
            pre_idx += _.end()
        elif _ := _assignment_reg.match(cur_str):
            token_str = _.group()
            ls.append(
                Assignment(lineno=lineno, offset=offset, text=text_ls[lineno - 1])
            )
            pre_idx += _.end()
        elif _ := _annotation_inline_reg.match(cur_str):
            token_str = _.group()
            if not ignore_annotations_and_whitespaces:
                ls.append(
                    Annotation(
                        token_str,
                        lineno=lineno,
                        offset=offset,
                        text=text_ls[lineno - 1],
                    )
                )
            pre_idx += _.end()
        elif _ := _unknown_reg.match(cur_str):
            raise SyntaxError("未知的词元")
        else:
            assert False
        lineno, offset = _calculate_lineno_and_offset(token_str, lineno, offset)

    return ls
