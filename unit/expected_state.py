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

        PARAMETER_STATE: 函数参数标识符 (语义分析器专用)
        FUNCTION_STATE:  期望函数标识符 (语义分析器专用)
        DEFINED_STATE:  期望已定义标识符 (语义分析器专用)
        UNIQUE_PARAM_STATE:  期望非重复的函数参数 (语义分析器专用)
    """

    IDENT_STATE = ()
    OPEN_PAREN_STATE = ()
    CLOSE_PAREN_STATE = ()
    COMMA_STATE = ()
    CONST_INT_STATE = ()
    FIN_STATE = ()
    CHECKED_FIN_STATE = ()

    PARAMETER_STATE = ()
    FUNCTION_STATE = ()
    DEFINED_STATE = ()
    UNIQUE_PARAM_STATE = ()

    UNKNOWN_STATE = ()
