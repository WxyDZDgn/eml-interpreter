from unit.token import _Token

from typing import Self


class _Node:
    def __init__(self, token: _Token, param_count: int = 0) -> None:
        self.token: _Token = token
        self.param_count: int = param_count
        self.params: list[_Node] = []

    def append(self, node: Self) -> None:
        if len(self.params) >= self.param_count:
            assert False
        self.params.append(node)
