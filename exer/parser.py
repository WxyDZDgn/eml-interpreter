from unit.token import (
    _Token,
    Comma,
    ConstInt,
    FuncEml,
    IdentVariable,
    Assignment,
    EndOfStmt,
    WhiteSpace,
    Annotation,
    OpenParen,
    CloseParen,
    ParameterVariable,
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
    """

    FUNC_NAME = auto()
    OPEN_PAREN = auto()
    IDENT_NAME = auto()
    CONST_INT = auto()
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
        s.append("参数名")
    if _ExpectedState.CONST_INT in state:
        s.append("常数")
    if _ExpectedState.COMMA in state:
        s.append("','")
    if _ExpectedState.CLOSE_PAREN in state:
        s.append("')'")
    if _ExpectedState.FIN_STATE in state:
        s.append("'='")
    return f"期望{'或'.join(s)}"


def _next_ignore_whitespaces_and_annotations(
    tokens: list[_Token], left: int, right: Optional[int] = None
) -> Optional[tuple[_Token, int]]:
    """
    解析下一个不被忽略的Token
    参数:
        left: 开始下标（闭区间）
        right: 结束下标（闭区间），默认为tokens长度

    返回:
        None: 超过范围的Token
        Tuple(
            _Token: 非忽略的词元
            int: 下一个需要解析的下标
        )
    """
    # 开区间闭区间可能有bug
    right = len(tokens) if right is None else (right + 1)
    for i in range(left, min(right, len(tokens))):
        cur = tokens[i]
        if isinstance(cur, WhiteSpace) or isinstance(cur, Annotation):
            continue
        return (cur, i + 1)
    return None


def _prev_ignore_whitespaces_and_annotations(
    tokens: list[_Token], right: Optional[int] = None, left: Optional[int] = None
) -> Optional[tuple[_Token, int]]:
    """
    解析上一个不被忽略的Token
    参数:
        right: 开始下标（闭区间）
        left: 结束下标（闭区间），默认为tokens长度

    返回:
        None: 超过范围的Token
        Tuple(
            _Token: 非忽略的词元
            int: 下一个需要解析的下标
        )
    """
    # 开区间闭区间可能有bug
    left = -1 if left is None else (left - 1)
    right = len(tokens) - 1 if right is None else right
    for i in range(right, max(left, -1), -1):
        cur = tokens[i]
        if isinstance(cur, WhiteSpace) or isinstance(cur, Annotation):
            continue
        return (cur, i - 1)
    return None


def _transfer_state_before_assignment(
    token: _Token, state: _ExpectedState
) -> _ExpectedState:
    """
    状态机状态转换（赋值词元前）

    规则:
        START       == FUNC_NAME
        FUNC_NAME   => OPEN_PAREN | FIN_STATE
        OPEN_PAREN  => CLOSE_PAREN | IDENT_NAME
        IDENT_NAME  => COMMA | CLOSE_PAREN
        COMMA       => IDENT_NAME
        CLOSE_PAREN => FIN_STATE
        FIN_STATE   => CHECKED_FIN_STATE
        END         == CHECKED_FIN_STATE
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


def _transfer_state_after_assignment(
    current_token: _Token, next_token: Optional[_Token], state: _ExpectedState
) -> _ExpectedState:
    """
    状态机状态转换（赋值词元后）

    规则:
    """
    raise NotImplementedError()


def _construct_node(
    variables: list[str],
    tokens: list[_Token],
    left: int,
    right: int,
    initial: bool = True,
) -> tuple[_Node, int]:
    state = (
        _ExpectedState.FUNC_NAME | _ExpectedState.CONST_INT | _ExpectedState.IDENT_NAME
    )
    tmp = _next_ignore_whitespaces_and_annotations(tokens, left, right)
    if tmp is None:
        raise SyntaxError(_syntax_error_message(state))
    cur, left_next = tmp
    tmp = _next_ignore_whitespaces_and_annotations(tokens, left_next, right)
    nxt = None if tmp is None else tmp[0]
    raise NotImplementedError()

    pass


def parser(code: str) -> list[_Node]:
    tokens = lexer(code)
    res = []
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
            root_node = _Node(tokens[cur_assignment_index], 2)
            # 处理赋值左边
            # func_name(x, y) = eml(eml(1, x), eml(y, 1));
            # ^^^^^^^^^^^^^^^^^
            variables: list[str] = []
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
                is_func_name = _ExpectedState.FUNC_NAME in state
                state = _transfer_state_before_assignment(cur, state)
                if is_ident:
                    para_name = cur.token_value
                    assert isinstance(para_name, str)
                    variables.append(para_name)
                if is_func_name:
                    func_token = cur
            left_node = _Node(func_token, len(variables))
            for _ in variables:
                left_node.append(_Node(ParameterVariable(_)))

            # 处理赋值右边
            # func_name(x, y) = eml(eml(1, x), eml(y, 1));
            #                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
            # `cur_assignment_index + 1` `right_index`
            right_node = _construct_node(
                variables, tokens, cur_assignment_index + 1, right_index
            )[0]

            root_node.append(left_node)
            root_node.append(right_node)
            res.append(root_node)
        else:
            # 无 '='

            raise NotImplementedError()

        # 结束部分
        left_index = right_index + 1
        if has_assignments_in_cur_stmt:
            cur_assignment_indexes_index += 1

    tmp = _next_ignore_whitespaces_and_annotations(tokens, left_index)
    if tmp is None:
        raise NotImplementedError()
        return res
    raise SyntaxError("未完成的Stmt")
