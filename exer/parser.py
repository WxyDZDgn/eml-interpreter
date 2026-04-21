from unit.token import (
    _Token,
    Comma,
    ConstInt,
    IdentVariable,
    Assignment,
    EndOfStmt,
    OpenParen,
    CloseParen,
)
from unit.node import _Node
from exer.lexer import lexer


from enum import Flag, auto


class _ExpectedState(Flag):
    """
    状态机判定期望解析的状态

    参数:
        IDENT_STATE: 期望标识符
        OPEN_PAREN_STATE: 期望'('
        CLOSE_PAREN_STATE: 期望')'
        COMMA_STATE: 期望','
        CONST_INT_STATE: 期望常数
        FIN_STATE: 期望'='或';'
        CHECKED_FIN_STATE: 检查完成
    """

    IDENT_STATE = auto()
    OPEN_PAREN_STATE = auto()
    CLOSE_PAREN_STATE = auto()
    COMMA_STATE = auto()
    CONST_INT_STATE = auto()
    FIN_STATE = auto()
    CHECKED_FIN_STATE = auto()

    pass


def _syntax_error_message(
    state: _ExpectedState,
    is_ignoring_before_or_after_assignment: bool = True,
    is_after_assignment: bool = True,
) -> str:
    """
    状态未达到期望的报错信息

    参数:
        state: 未达到的期望
        is_ignoring_before_or_after_assignment: 是否需要区分'='和';'
        is_after_assignment: 若为 True 则期望';', 否则期望'='

    返回:
        str, 基于未达到期望的状态返回报错信息
    """
    s = []
    if _ExpectedState.IDENT_STATE in state:
        s.append("标识符")
    if _ExpectedState.OPEN_PAREN_STATE in state:
        s.append("'('")
    if _ExpectedState.CLOSE_PAREN_STATE in state:
        s.append("')'")
    if _ExpectedState.COMMA_STATE in state:
        s.append("','")
    if _ExpectedState.CONST_INT_STATE in state:
        s.append("常数")
    if _ExpectedState.FIN_STATE in state:
        if is_ignoring_before_or_after_assignment or not is_after_assignment:
            s.append("'='")
        if is_ignoring_before_or_after_assignment or is_after_assignment:
            s.append("';'")
    return f"期望{'或'.join(s)}"


def _transfer_state(
    state: _ExpectedState,
    token: _Token,
    length_of_stack: int,
    is_ignoring_before_or_after_assignment: bool = True,
) -> _ExpectedState:
    """
    状态机状态转换（赋值词元后）

    参数:
        state: 当前期望状态
        token: 当前词元
        length_of_stack: 函数栈长度（除去根）
        is_ignoring_before_or_after_assignment: 用于细化报错信息, 见 `_syntax_error_message`

    返回:
        _ExpectedState: 返回下一个的期望状态

    规则:
        IDENT_STATE       => OPEN_PAREN_STATE
                           | CLOSE_PAREN_STATE
                           | COMMA_STATE
                           | FIN_STATE
        OPEN_PAREN_STATE  => IDENT_STATE
                           | CLOSE_PAREN_STATE
                           | CONST_INT_STATE
        CLOSE_PAREN_STATE => CLOSE_PAREN_STATE
                           | COMMA_STATE
                           | FIN_STATE
        COMMA_STATE       => IDENT_STATE
                           | CONST_INT_STATE
        CONST_INT_STATE   => CLOSE_PAREN_STATE
                           | COMMA_STATE
                           | FIN_STATE
        FIN_STATE         => IDENT_STATE
                           | CONST_INT_STATE | CHECKED_FIN_STATE
    """
    is_stack_empty = length_of_stack <= 0
    if isinstance(token, IdentVariable):
        if _ExpectedState.IDENT_STATE in state:
            if is_stack_empty:
                return _ExpectedState.OPEN_PAREN_STATE | _ExpectedState.FIN_STATE
            return (
                _ExpectedState.OPEN_PAREN_STATE
                | _ExpectedState.CLOSE_PAREN_STATE
                | _ExpectedState.COMMA_STATE
            )
    if isinstance(token, OpenParen):
        if _ExpectedState.OPEN_PAREN_STATE in state:
            return (
                _ExpectedState.IDENT_STATE
                | _ExpectedState.CLOSE_PAREN_STATE
                | _ExpectedState.CONST_INT_STATE
            )
    if isinstance(token, CloseParen):
        if _ExpectedState.CLOSE_PAREN_STATE in state:
            assert length_of_stack >= 1
            if length_of_stack <= 1:
                return _ExpectedState.FIN_STATE
            return _ExpectedState.CLOSE_PAREN_STATE | _ExpectedState.COMMA_STATE
    if isinstance(token, Comma):
        if _ExpectedState.COMMA_STATE in state:
            assert not is_stack_empty
            return _ExpectedState.IDENT_STATE | _ExpectedState.CONST_INT_STATE
    if isinstance(token, ConstInt):
        if _ExpectedState.CONST_INT_STATE in state:
            if is_stack_empty:
                return _ExpectedState.FIN_STATE
            return _ExpectedState.CLOSE_PAREN_STATE | _ExpectedState.COMMA_STATE
    if isinstance(token, Assignment):
        if _ExpectedState.FIN_STATE in state:
            assert is_stack_empty
            return _ExpectedState.IDENT_STATE | _ExpectedState.CONST_INT_STATE
    if isinstance(token, EndOfStmt):
        if _ExpectedState.FIN_STATE in state:
            assert is_stack_empty
            return _ExpectedState.CHECKED_FIN_STATE
    raise SyntaxError(
        _syntax_error_message(state, is_ignoring_before_or_after_assignment)
    )


def _construct_node(tokens: list[_Token], left: int, right: int) -> _Node:
    """
    根据下标在闭区间 [left, right] 区间内的词元构造 AST

    参数:
        tokens: 词法分析器返回的词元列表
        left: 处理的最左词元的下标
        right: 处理的最右词元的下标

    返回:
        _Node: AST 节点
    """
    assert 0 <= left <= right < len(tokens)

    stack: list[tuple[_Node, list[_Token]]] = [(_Node(Assignment()), [])]
    state = _ExpectedState.IDENT_STATE
    is_ignoring_before_or_after_assignment = True
    for i in range(left, right + 1):
        cur = tokens[i]
        state = _transfer_state(
            state, cur, len(stack) - 1, is_ignoring_before_or_after_assignment
        )
        if isinstance(cur, Assignment):
            is_ignoring_before_or_after_assignment = False
        if isinstance(cur, CloseParen):
            *stack, _ = stack
            root, param = _
            for p in param:
                root.append(_Node(p))
            stack[-1][0].append(root)
            continue
        if isinstance(cur, IdentVariable) or isinstance(cur, ConstInt):
            stack[-1][1].append(cur)
        if isinstance(cur, OpenParen):
            assert left < i
            stack.append((_Node(tokens[i - 1]), []))

    if not (_ExpectedState.CHECKED_FIN_STATE in state):
        raise SyntaxError(
            _syntax_error_message(state, is_ignoring_before_or_after_assignment)
        )
    assert len(stack) == 1
    assert isinstance(tokens[right], EndOfStmt)
    return stack[0][0]


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
    tokens = lexer(code)
    res = []
    last_end_of_stmt_index = 0
    for i in range(len(tokens)):
        if isinstance(tokens[i], EndOfStmt):
            res.append(_construct_node(tokens, last_end_of_stmt_index, i))
            last_end_of_stmt_index = i + 1
    if last_end_of_stmt_index < len(tokens):
        res.append(_construct_node(tokens, last_end_of_stmt_index, len(tokens) - 1))
    return res
