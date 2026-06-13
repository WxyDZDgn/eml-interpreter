from flags import Flags


class ExpectedState(Flags):
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

    IDENT_STATE = ()
    OPEN_PAREN_STATE = ()
    CLOSE_PAREN_STATE = ()
    COMMA_STATE = ()
    CONST_INT_STATE = ()
    FIN_STATE = ()
    CHECKED_FIN_STATE = ()

    UNKNOWN_STATE = ()
