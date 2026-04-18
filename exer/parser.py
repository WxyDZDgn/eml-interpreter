from unit.token import FuncEml, IdentVariable, Assignment, EndOfStmt
from unit.node import _Node
from exer.lexer import lexer


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
        for index in range(len(tokens)):
            cur = tokens[index]
            match cur:
                case _ if isinstance(cur, EndOfStmt):
                    end_of_stmt_indexes.append(index)
                case _ if isinstance(cur, Assignment):
                    assignment_indexes.append(index)

        print(tokens)
        print(end_of_stmt_indexes)
        print(assignment_indexes)
        return []

    pass
