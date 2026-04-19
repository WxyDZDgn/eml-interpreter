from unit.token import (
    _Token,
    Comma,
    FuncEml,
    IdentVariable,
    Assignment,
    EndOfStmt,
    WhiteSpace,
    Annotation,
    OpenParen,
    CloseParen,
)
from unit.node import _Node
from exer.lexer import lexer


from enum import Flag, auto
from typing import Optional


class _ExpectedState(Flag):
    """
    状态机判定期望解析的状态

    参数:
        FUNC_NAME: 期望为'函数名'
        OPEN_PAREN: 期望为'('
        IDENT_NAME: 期望为'参数名'
        COMMA: 期望为','
        CLOSE_PAREN: 期望为')'
        FIN_STATE: 期望为'='
        CHECKED_FIN_STATE: 检查完毕

    规则:
        START == FUNC_NAME
        FUNC_NAME   => OPEN_PAREN | FIN_STATE
        OPEN_PAREN  => CLOSE_PAREN | IDENT_NAME
        IDENT_NAME  => COMMA | CLOSE_PAREN
        COMMA       => IDENT_NAME
        CLOSE_PAREN => FIN_STATE
        FIN_STATE   => CHECKED_FIN_STATE
        END == CHECKED_FIN_STATE
    """
    FUNC_NAME = auto()
    OPEN_PAREN = auto()
    IDENT_NAME = auto()
    COMMA = auto()
    CLOSE_PAREN = auto()
    FIN_STATE = auto()
    CHECKED_FIN_STATE = auto()


def _syntax_error_message(state: _ExpectedState) -> str:
    """
    状态未达到期望的报错信息
    """
    s = []
    if _ExpectedState.FUNC_NAME in state:
        s.append("函数名")
    if _ExpectedState.OPEN_PAREN in state:
        s.append("'('")
    if _ExpectedState.IDENT_NAME in state:
        s.append("'参数名'")
    if _ExpectedState.COMMA in state:
        s.append("','")
    if _ExpectedState.CLOSE_PAREN in state:
        s.append("')'")
    if _ExpectedState.FIN_STATE in state:
        s.append("'='")
    return f"期望{'或'.join(s)}"


def _next_ignore_whitespaces_and_annotations(
    tokens: list[_Token], start: int, end: Optional[int] = None
) -> Optional[tuple[_Token, int]]:
    """
    解析下一个不被忽略的Token
    参数:
        start: 开始下标（闭区间）
        end: 结束下标（闭区间），默认为tokens长度

    返回:
        None: 超过范围的Token
        Tuple(
            _Token: 非忽略的词元
            int: 下一个需要解析的下标
        )
    """
    # 开区间闭区间可能有bug
    end = len(tokens) if end is None else (end + 1)
    for i in range(start, end):
        cur = tokens[i]
        if isinstance(cur, WhiteSpace) or isinstance(cur, Annotation):
            continue
        return (cur, i + 1)
    return None


def _transfer_state_before_assignment(token: _Token, state: _ExpectedState) -> _ExpectedState:
    """
    状态机状态转换
    """
    if isinstance(token, IdentVariable):
        if _ExpectedState.FUNC_NAME in state:
            return _ExpectedState.OPEN_PAREN | _ExpectedState.FIN_STATE
        if _ExpectedState.IDENT_NAME in state:
            return _ExpectedState.COMMA | _ExpectedState.CLOSE_PAREN
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(token, OpenParen):
        if _ExpectedState.OPEN_PAREN in state:
            return _ExpectedState.IDENT_NAME | _ExpectedState.CLOSE_PAREN
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(token, Comma):
        if _ExpectedState.COMMA in state:
            return _ExpectedState.IDENT_NAME
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(token, CloseParen):
        if _ExpectedState.CLOSE_PAREN in state:
            return _ExpectedState.FIN_STATE
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(token, Assignment):
        if _ExpectedState.FIN_STATE in state:
            return _ExpectedState.CHECKED_FIN_STATE
        raise SyntaxError(_syntax_error_message(state))
    else:
        assert False


class Parser:
    def __init__(self) -> None:
        # (名称, 参数数量) -> (有效位, 可修改, AST)
        self.symbol_table: dict[tuple[str, int], tuple[bool, bool, _Node]] = {}
        self._init_eml()

    def _init_eml(self) -> None:
        eml = _Node(FuncEml(), 2)
        eml.append(_Node(IdentVariable("x")))
        eml.append(_Node(IdentVariable("y")))
        self.symbol_table[("eml", 2)] = (True, False, eml)

    def exec(self, code: str) -> list[str]:
        tokens = lexer(code)
        # 暂时不支持赋值
        end_of_stmt_indexes = []
        assignment_indexes = []
        left_index = 0
        cur_assignment_indexes_index = 0
        for index in range(len(tokens)):
            cur = tokens[index]
            match cur:
                case _ if isinstance(cur, EndOfStmt):
                    end_of_stmt_indexes.append(index)
                case _ if isinstance(cur, Assignment):
                    assignment_indexes.append(index)

        for right_index in end_of_stmt_indexes:
            has_assignments_in_cur_stmt = False
            for i in range(cur_assignment_indexes_index, len(assignment_indexes)):
                if assignment_indexes[i] < right_index:
                    if has_assignments_in_cur_stmt:
                        raise SyntaxError("同一个语句中不支持多个'='")
                    has_assignments_in_cur_stmt = True
                elif assignment_indexes[i] > right_index:
                    break
                else:
                    assert False, "不期望的分支"

            if has_assignments_in_cur_stmt:
                # 有 '='

                # 处理赋值左边
                # func_name(x, y) = eml(eml(1, x), eml(y, 1));
                # ^^^^^^^^^^^^^^^^^
                variables = []
                cur_assignment_index = assignment_indexes[cur_assignment_indexes_index]
                state = _ExpectedState.FUNC_NAME
                while _ExpectedState.CHECKED_FIN_STATE not in state:
                    tmp = _next_ignore_whitespaces_and_annotations(
                        tokens, left_index, cur_assignment_index
                    )
                    if tmp is None:
                        raise SyntaxError(_syntax_error_message(state))
                    cur, left_index = tmp
                    is_ident = _ExpectedState.IDENT_NAME in state
                    state = _transfer_state_before_assignment(cur, state)
                    if is_ident:
                        variables.append(cur)

                # 处理赋值右边
                # func_name(x, y) = eml(eml(1, x), eml(y, 1));
                #                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
                tmp = _next_ignore_whitespaces_and_annotations(
                    tokens, left_index, cur_assignment_index
                )
                print(variables)
                raise NotImplementedError()
            else:
                # 无 '='

                raise NotImplementedError()

            # 结束部分
            left_index = right_index + 1
            if has_assignments_in_cur_stmt:
                cur_assignment_indexes_index += 1

        tmp = _next_ignore_whitespaces_and_annotations(tokens, left_index)
        if tmp is None:
            return []
        raise SyntaxError("未完成的Stmt")

    pass
