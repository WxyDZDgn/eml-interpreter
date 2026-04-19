from unit.node import _Node

class Executer:
    def __init__(self) -> None:
        # (名称, 参数数量) -> (有效位, 可修改, AST)
        self.symbol_table: dict[tuple[str, int], tuple[bool, bool, _Node]] = {}
        pass
