from unit.token import (
    FuncEml,
    IdentVariable,
    Assignment,
    EndOfStmt,
    WhiteSpace,
    Annotation,
)
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
                        assert False, "同一个语句中不支持多个'='"
                    has_assignments_in_cur_stmt = True
                elif assignment_indexes[i] > right_index:
                    break
                else:
                    assert False, "不期望的分支"

            # TODO: 还没结束

            # 结束部分
            left_index = right_index + 1
            if has_assignments_in_cur_stmt:
                cur_assignment_indexes_index += 1

        for index in range(left_index, len(tokens)):
            cur = tokens[index]
            if isinstance(cur, WhiteSpace) or isinstance(cur, Annotation):
                continue
            assert False, "未完成的Stmt"
        return []

    pass
