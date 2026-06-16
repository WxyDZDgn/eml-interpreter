# @Time : 2026/6/15 09:37
# @Author : Whania
# @FileName: symbol_table.py
from typing import Optional

from unit.node import Node
from unit.token import Token


class SymbolTable:
    """
    符号表

    属性:
        table: 封装字典作为符号表(Token, 参数数量) -> (有效位, 可修改, AST_Node, Token)

    """

    # 不确定 ident_name 要不要用 Token 或者 Node 代替，后者甚至包括 parameter_count
    def __init__(self):
        self.table: dict[tuple[Token, int], tuple[bool, bool, Optional[Node], Token]] = dict()

    def is_defined(self, ident_token: Token, parameter_count: int) -> bool:
        tmp = (ident_token, parameter_count)
        return tmp in self.table and self.table[tmp][0]

    def is_modifiable(self, ident_token: Token, parameter_count: int) -> bool:
        tmp = (ident_token, parameter_count)
        return self.is_defined(*tmp) and self.table[tmp][1]

    def clear(self):
        # 本打算直接修改有效位的，鉴于元组无法修改，并且没想好显式指定类型到定长可修改结构，先暂时 `.clear()`
        self.table.clear()

    def put(self, ident_token: Token, parameter_count: int, is_modifiable: bool = True,
            ast_node: Optional[Node] = None) -> bool:
        tmp = (ident_token, parameter_count)
        if self.is_defined(*tmp):
            if not self.is_modifiable(*tmp):
                return False
            assert is_modifiable == self.is_modifiable(*tmp)
        self.table[tmp] = (True, is_modifiable, ast_node, tmp[0])
        return True

    def get(self, ident_token: Token, parameter_count: int) -> Optional[Node]:
        if not self.is_defined(ident_token, parameter_count):
            return None
        return self.table[(ident_token, parameter_count)][2]

    def get_recycle(self, ident_token: Token, parameter_count: int) -> Optional[Token]:
        if not self.is_defined(ident_token, parameter_count):
            return None
        return self.table[(ident_token, parameter_count)][3]

    def __contains__(self, item: Node) -> bool:
        token, count = item.token, len(item.params)
        return (token, count) in self.table
