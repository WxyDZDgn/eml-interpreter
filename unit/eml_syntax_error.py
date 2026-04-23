from unit.expected_state import ExpectedState
from unit.token import _Token, Unknown


def _syntax_error_message(
    state: ExpectedState,
    is_ignoring_before_or_after_assignment: bool,
    is_after_assignment: bool,
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
    if ExpectedState.UNKNOWN_STATE in state:
        return f"未知的词元"
    s = []
    if ExpectedState.IDENT_STATE in state:
        s.append("标识符")
    if ExpectedState.OPEN_PAREN_STATE in state:
        s.append("'('")
    if ExpectedState.CLOSE_PAREN_STATE in state:
        s.append("')'")
    if ExpectedState.COMMA_STATE in state:
        s.append("','")
    if ExpectedState.CONST_INT_STATE in state:
        s.append("常数")
    if ExpectedState.FIN_STATE in state:
        if is_ignoring_before_or_after_assignment or not is_after_assignment:
            s.append("'='")
        if is_ignoring_before_or_after_assignment or is_after_assignment:
            s.append("';'")
    return f"期望{'或'.join(s)}"


def raise_syntax_error(
    state: ExpectedState,
    token: _Token,
    is_ignoring_before_or_after_assignment: bool = True,
    is_after_assignment: bool = True,
) -> None:
    raise SyntaxError(
        _syntax_error_message(
            ExpectedState.UNKNOWN_STATE if isinstance(token, Unknown) else state,
            is_ignoring_before_or_after_assignment,
            is_after_assignment,
        ),
        token.info,
    )
