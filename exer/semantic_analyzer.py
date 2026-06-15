from exer.parser import parser
from unit.node import Node
from unit.symbol_table import SymbolTable
from unit.token import Execute, Assignment


def _semantic_recursive(root: Node, is_after_assignment: bool,
                        symbol_tables: list[SymbolTable]) -> Node:
    pass


def semantic_analyzer(code: str) -> Node:
    """
        语义分析器，根据 AST 节点列表整合成一个 AST，对节点进行专有优化，并同时检查语义错误

        参数:
            code: 代码片段

        返回:
            Node: AST 根节点
        """
    nodes = parser(code)
    root = Node(Execute())
    symbol_tables: list[SymbolTable] = []
    for node in nodes:
        # 在这里检查语义
        if isinstance(node.token, Assignment):
            assert len(node.params) == 2
            node.params[0] = _semantic_recursive(node.params[0], False, symbol_tables)
            node.params[1] = _semantic_recursive(node.params[1], True, symbol_tables)
        else:
            node = _semantic_recursive(node, True, symbol_tables)
            pass
        root.append(node)
    return root
