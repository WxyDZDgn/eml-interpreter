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
    Unknown,
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
_annotation_inline_reg = re.compile(r"//[^\n]+")
_unknown_reg = re.compile(r"[^0-9a-zA-Z_(),;=/]+")


def lexer(code: str) -> list[_Token]:
    ls = []
    pre_idx = 0

    while pre_idx < len(code):
        cur_str = code[pre_idx:]
        if _ := _text_reg.match(cur_str):
            ls.append(IdentVariable(_.group()))
            pre_idx += _.end()
        elif _ := _number_reg.match(cur_str):
            ls.append(ConstInt(int(_.group())))
            pre_idx += _.end()
        elif _ := _open_paren_reg.match(cur_str):
            ls.append(OpenParen())
            pre_idx += _.end()
        elif _ := _close_paren_reg.match(cur_str):
            ls.append(CloseParen())
            pre_idx += _.end()
        elif _ := _comma_reg.match(cur_str):
            ls.append(Comma())
            pre_idx += _.end()
        elif _ := _end_of_stmt_reg.match(cur_str):
            ls.append(EndOfStmt())
            pre_idx += _.end()
        elif _ := _white_space_reg.match(cur_str):
            ls.append(WhiteSpace(_.group()))
            pre_idx += _.end()
        elif _ := _assignment_reg.match(cur_str):
            ls.append(Assignment())
            pre_idx += _.end()
        elif _ := _annotation_inline_reg.match(cur_str):
            # 忽略注释, 不传递词元
            # ls.append(Annotation(_.group()))
            pre_idx += _.end()
        elif _ := _unknown_reg.match(cur_str):
            ls.append(Unknown(_.group()))
            pre_idx += _.end()
        else:
            assert False

    return ls
