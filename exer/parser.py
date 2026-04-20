from unit.token import (
    _Token,
    Comma,
    ConstInt,
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
        FUNC_NAME: 期望为'函数名'，下一个词元严格是'('
        OPEN_PAREN: 期望为'('
        IDENT_NAME: 期望为'参数名'
        COMMA: 期望为','
        CLOSE_PAREN: 期望为')'
        FIN_STATE: 期望为'='
        CHECKED_FIN_STATE: 检查完毕

        ENTER_RECURSION: 进入递归（右解析专用）
        OUTER_RECURSION: 退出递归（右解析专用）
    """

    FUNC_NAME = auto()
    OPEN_PAREN = auto()
    IDENT_NAME = auto()
    CONST_INT = auto()
    COMMA = auto()
    CLOSE_PAREN = auto()
    FIN_STATE = auto()
    CHECKED_FIN_STATE = auto()

    ENTER_RECURSION = auto()
    OUTER_RECURSION = auto()


def _syntax_error_message(state: _ExpectedState) -> str:
    """
    状态未达到期望的报错信息

    参数:
        state: 未达到的期望

    返回:
        str, 基于未达到期望的状态返回报错信息
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
        s.append("';'")
    return f"期望{'或'.join(s)}"


def _has_next_ignore_whitespaces_and_annotations(
    tokens: list[_Token], left: int, right: Optional[int] = None
) -> bool:
    """
    判断下一个不被忽略的Token是否存在
    参数:
        left: 开始下标（闭区间）
        right: 结束下标（闭区间），默认为tokens长度

    返回:
        True: 表明 [left, right] 内有除了空白和注释词元之外的词元
    """
    # 开区间闭区间可能有bug
    right = len(tokens) if right is None else (right + 1)
    for i in range(left, min(right, len(tokens))):
        cur = tokens[i]
        if isinstance(cur, WhiteSpace) or isinstance(cur, Annotation):
            continue
        return True
    return False


def _next_ignore_whitespaces_and_annotations(
    tokens: list[_Token], left: int, right: Optional[int] = None
) -> tuple[_Token, int]:
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
    assert False


def _transfer_state(
    current_token: _Token, next_token: _Token, state: _ExpectedState, initial: bool
) -> _ExpectedState:
    """
    状态机状态转换（赋值词元后）

    规则:
        TODO:
    """
    if isinstance(current_token, OpenParen):
        if isinstance(next_token, CloseParen):
            return _ExpectedState.CLOSE_PAREN
        if _ExpectedState.OPEN_PAREN in state:
            if initial:
                return _ExpectedState.ENTER_RECURSION | _ExpectedState.FIN_STATE
            return (
                _ExpectedState.ENTER_RECURSION
                | _ExpectedState.CLOSE_PAREN
                | _ExpectedState.COMMA
            )
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, CloseParen):
        if _ExpectedState.CLOSE_PAREN in state:
            if initial:
                return _ExpectedState.FIN_STATE
            return _ExpectedState.OUTER_RECURSION
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, Comma):
        if _ExpectedState.COMMA in state:
            return (
                _ExpectedState.IDENT_NAME
                | _ExpectedState.CONST_INT
                | _ExpectedState.FUNC_NAME
            )
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, ConstInt):
        if _ExpectedState.CONST_INT in state:
            if initial:
                return _ExpectedState.FIN_STATE
            else:
                return _ExpectedState.COMMA | _ExpectedState.CLOSE_PAREN
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, IdentVariable):
        if isinstance(next_token, OpenParen):
            if _ExpectedState.FUNC_NAME in state:
                return _ExpectedState.OPEN_PAREN
            raise SyntaxError(_syntax_error_message(state))
        if _ExpectedState.IDENT_NAME in state:
            if initial:
                return _ExpectedState.FIN_STATE
            return _ExpectedState.COMMA | _ExpectedState.CLOSE_PAREN
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, Assignment):
        if _ExpectedState.FIN_STATE:
            return _ExpectedState.CHECKED_FIN_STATE
        raise SyntaxError(_syntax_error_message(state))
    elif isinstance(current_token, EndOfStmt):
        if _ExpectedState.FIN_STATE:
            return _ExpectedState.CHECKED_FIN_STATE
        raise SyntaxError(_syntax_error_message(state))
    else:
        assert False


def _construct_node(
    tokens: list[_Token],
    left: int,
    right: int,
    initial: bool = True,
) -> tuple[_Node, int]:
    """
    根据下标在闭区间 [left, right] 区间内的词元构造 AST

    参数:
        tokens: 词法分析器返回的词元列表
        left: 处理的最左词元的下标
        right: 处理的最右词元的下标
        initial: 是否第一次运行函数（是则表示当前为递归第一层，否则为其他层）

    返回:
        Tuple(
            _Node: AST 节点
            int: 完成后下一步该处理的 Token 对应下标
        )
    """
    state: _ExpectedState = (
        (
            _ExpectedState.CONST_INT
            | _ExpectedState.FUNC_NAME
            | _ExpectedState.IDENT_NAME
        )
        if initial
        else (
            _ExpectedState.CONST_INT
            | _ExpectedState.FUNC_NAME
            | _ExpectedState.IDENT_NAME
            | _ExpectedState.OUTER_RECURSION
        )
    )
    root: Optional[_Token] = None
    parameters: list[_Node] = []
    changed = False
    while True:
        tmp = _next_ignore_whitespaces_and_annotations(tokens, left, right)
        cur, left = tmp
        if root is None:
            root = cur
        if isinstance(cur, EndOfStmt) or isinstance(cur, Assignment):
            if not initial:
                raise SyntaxError("未完成的')'")
            if not changed:
                raise SyntaxError(_syntax_error_message(state))
            break
        changed = True
        tmp = _next_ignore_whitespaces_and_annotations(tokens, left, right)
        nxt, _ = tmp
        state = _transfer_state(cur, nxt, state, initial)
        # 是函数导致的期望是'('，准备递归
        if _ExpectedState.OUTER_RECURSION in state:
            break
        if _ExpectedState.ENTER_RECURSION in state:
            tmp = _construct_node(tokens, left, right, False)
            parameters.append(tmp[0])
            left = tmp[1]
            continue
        if _ExpectedState.COMMA in state or _ExpectedState.CLOSE_PAREN in state:
            parameters.append(_Node(cur))
    assert root is not None
    res = _Node(root, len(parameters))
    for each in parameters:
        res.append(each)
    return (res, left)


def parser(code: str) -> list[_Node]:
    """
    语法分析器，根据代码分析格式并为每一条 Stmt 得到一个 AST，组合返回一个列表

    参数:
        code: 代码片段

    返回:
        list[
            _Node: 单个 Stmt 的 AST 结构
        ]: 所有 Stmt 的 AST
    """
    tokens: list[_Token] = lexer(code)
    res: list[_Node] = []
    end_of_stmt_indexes: list[int] = []
    assignment_indexes: list[int] = []
    left_index = 0
    cur_assignment_indexes_index = 0
    for index in range(len(tokens)):
        cur = tokens[index]
        if isinstance(cur, EndOfStmt):
            end_of_stmt_indexes.append(index)
        if isinstance(cur, Assignment):
            assignment_indexes.append(index)

    if len(tokens) <= 0:
        raise SyntaxError("空代码")

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
            cur_assignment_index = assignment_indexes[cur_assignment_indexes_index]
            # 有 '='
            root_node = _Node(tokens[cur_assignment_index], 2)
            # 处理赋值左边
            # func_name(x, y) = eml(eml(1, x), eml(y, 1));
            # ^^^^^^^^^^^^^^^^^
            left_node = _construct_node(tokens, left_index, cur_assignment_index)[0]
            # 处理赋值右边
            # func_name(x, y) = eml(eml(1, x), eml(y, 1));
            #                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
            # `cur_assignment_index + 1` `right_index`
            right_node = _construct_node(tokens, cur_assignment_index + 1, right_index)[
                0
            ]

            root_node.append(left_node)
            root_node.append(right_node)
            res.append(root_node)
        else:
            # 无 '='
            res.append(_construct_node(tokens, left_index, right_index, True)[0])

        # 结束部分
        left_index = right_index + 1
        if has_assignments_in_cur_stmt:
            cur_assignment_indexes_index += 1

    if len(end_of_stmt_indexes) <= 0 or _has_next_ignore_whitespaces_and_annotations(
        tokens, end_of_stmt_indexes[-1] + 1
    ):
        raise SyntaxError("未完成的Stmt")
    return res
