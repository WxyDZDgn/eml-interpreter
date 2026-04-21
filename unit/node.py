from unit.token import _Token

from typing import Self


class _Node:
    def __init__(self, token: _Token, param_count: int = 0) -> None:
        self.token: _Token = token
        self.params: list[_Node] = []

    def append(self, node: Self) -> None:
        self.params.append(node)

    def __repr__(self) -> str:
        return f"<Node: '{str(self.token)}' [{', '.join(list(map(str, self.params)))}]>"
    