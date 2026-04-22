from enum import Flag, auto


class ExpectedState(Flag):
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

    UNKNOWN_STATE = auto()

    pass