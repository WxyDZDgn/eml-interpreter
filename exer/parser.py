from unit.eml_syntax_error import raise_syntax_error
from unit.expected_state import ExpectedState
from unit.token import (
    Token,
    Comma,
    ConstInt,
    IdentVariable,
    Assignment,
    EndOfStmt,
    OpenParen,
    CloseParen,
)
from unit.node import Node
from exer.lexer import lexer

from typing import Optional


def _transfer_state(
        state: ExpectedState,
        token: Token,
        length_of_stack: int,
        is_ignoring_before_or_after_assignment: bool = True,
) -> ExpectedState:
    """
    状态机状态转换（赋值词元后）

    参数:
        state: 当前期望状态
        token: 当前词元
        length_of_stack: 函数栈长度（除去根）
        is_ignoring_before_or_after_assignment: 用于细化报错信息, 见 `_syntax_error_message`

    返回:
        ExpectedState: 返回下一个的期望状态

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
        if ExpectedState.IDENT_STATE in state:
            if is_stack_empty:
                return ExpectedState.OPEN_PAREN_STATE | ExpectedState.FIN_STATE
            return (
                    ExpectedState.OPEN_PAREN_STATE
                    | ExpectedState.CLOSE_PAREN_STATE
                    | ExpectedState.COMMA_STATE
            )
    if isinstance(token, OpenParen):
        if ExpectedState.OPEN_PAREN_STATE in state:
            return (
                    ExpectedState.IDENT_STATE
                    | ExpectedState.CLOSE_PAREN_STATE
                    | ExpectedState.CONST_INT_STATE
            )
    if isinstance(token, CloseParen):
        if ExpectedState.CLOSE_PAREN_STATE in state:
            assert length_of_stack >= 1
            if length_of_stack <= 1:
                return ExpectedState.FIN_STATE
            return ExpectedState.CLOSE_PAREN_STATE | ExpectedState.COMMA_STATE
    if isinstance(token, Comma):
        if ExpectedState.COMMA_STATE in state:
            assert not is_stack_empty
            return ExpectedState.IDENT_STATE | ExpectedState.CONST_INT_STATE
    if isinstance(token, ConstInt):
        if ExpectedState.CONST_INT_STATE in state:
            if is_stack_empty:
                return ExpectedState.FIN_STATE
            return ExpectedState.CLOSE_PAREN_STATE | ExpectedState.COMMA_STATE
    if isinstance(token, Assignment):
        if ExpectedState.FIN_STATE in state:
            assert is_stack_empty
            return ExpectedState.IDENT_STATE | ExpectedState.CONST_INT_STATE
    if isinstance(token, EndOfStmt):
        if ExpectedState.FIN_STATE in state:
            assert is_stack_empty
            return ExpectedState.CHECKED_FIN_STATE

    raise_syntax_error(state, token, is_ignoring_before_or_after_assignment)
    assert False


def _construct_node(tokens: list[Token], left: int, right: int) -> Node:
    """
    根据下标在闭区间 [left, right] 区间内的词元构造 AST

    参数:
        tokens: 词法分析器返回的词元列表
        left: 处理的最左词元的下标
        right: 处理的最右词元的下标

    返回:
        Node: AST 节点
    """
    assert 0 <= left <= right < len(tokens)

    stack: list[tuple[Node, list[Token]]] = [(Node(), [])]
    state = ExpectedState.IDENT_STATE
    is_ignoring_before_or_after_assignment = True
    root_token: Optional[Token] = None
    for i in range(left, right + 1):
        cur = tokens[i]
        state = _transfer_state(
            state, cur, len(stack) - 1, is_ignoring_before_or_after_assignment
        )
        if isinstance(cur, EndOfStmt):
            assert i >= right
        if root_token is None:
            root_token = cur
        if isinstance(cur, Assignment):
            root_token = cur
            is_ignoring_before_or_after_assignment = False
        if isinstance(cur, CloseParen):
            *stack, _ = stack
            root, param = _
            for p in param:
                root.append(Node(p))
            stack[-1][0].append(root)
            continue
        if isinstance(cur, IdentVariable) or isinstance(cur, ConstInt):
            stack[-1][1].append(cur)
        if isinstance(cur, OpenParen):
            assert left < i
            stack.append((Node(tokens[i - 1]), []))

    if not (ExpectedState.CHECKED_FIN_STATE in state):
        raise_syntax_error(state, tokens[right], is_ignoring_before_or_after_assignment)
    assert len(stack) == 1
    assert isinstance(tokens[right], EndOfStmt)
    stack[0][0].token = root_token
    return stack[0][0]


def parser(code: str) -> list[Node]:
    """
    语法分析器，根据代码分析格式并为每一条 Stmt 得到一个 AST，组合返回一个列表

    参数:
        code: 代码片段

    返回:
        list[
            Node: 单个 Stmt 的 AST 结构
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
