from unit.token import _Token

from typing import Self, Optional


class _Node:
    def __init__(self, token: Optional[_Token] = None) -> None:
        self.token: Optional[_Token] = token
        self.params: list[_Node] = []
        

    def append(self, node: Self) -> None:
        self.params.append(node)

    def __repr__(self) -> str:
        return f"<Node: '{str(self.token)}' [{', '.join(list(map(str, self.params)))}]>"
    