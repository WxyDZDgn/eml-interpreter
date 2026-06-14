from exer.parser import parser
from unit.node import Node
from unit.token import Execute


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
    for node in nodes:
        # 在这里检查语义
        root.append(node)
    return root
