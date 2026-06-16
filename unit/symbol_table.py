# @Time : 2026/6/15 09:37
# @Author : Whania
# @FileName: symbol_table.py
from typing import Optional

from unit.node import Node


class SymbolTable:
    """
    符号表

    属性:
        table: 封装字典作为符号表(名称, 参数数量) -> (有效位, 可修改, AST_Node)

    """

    # 不确定 ident_name 要不要用 Token 或者 Node 代替，后者甚至包括 parameter_count
    def __init__(self):
        self.table: dict[tuple[str, int], tuple[bool, bool, Optional[Node]]] = dict()

    def is_defined(self, ident_name: str, parameter_count: int) -> bool:
        tmp = (ident_name, parameter_count)
        return tmp in self.table.keys() and self.table[tmp][0]

    def is_modifiable(self, ident_name: str, parameter_count: int) -> bool:
        tmp = (ident_name, parameter_count)
        return self.is_defined(*tmp) and self.table[tmp][1]

    def clear(self):
        # 本打算直接修改有效位的，鉴于元组无法修改，并且没想好显式指定类型到定长可修改结构，先暂时 `.clear()`
        self.table.clear()

    def put(self, ident_name: str, parameter_count: int, is_modifiable: bool = True,
            ast_node: Optional[Node] = None) -> bool:
        if self.is_defined(ident_name, parameter_count) and not self.is_modifiable(ident_name, parameter_count):
            return False
        tmp = (ident_name, parameter_count)
        assert tmp not in self.table.keys() or self.table[tmp][1] == is_modifiable
        self.table[tmp] = (True, is_modifiable, ast_node)
        return True

    def get(self, ident_name: str, parameter_count: int) -> Optional[Node]:
        if not self.is_defined(ident_name, parameter_count):
            return None
        return self.table[(ident_name, parameter_count)][2]
