from unit.token import Token

from typing import Self, Optional


class Node:
    def __init__(self, token: Optional[Token] = None) -> None:
        self.token: Optional[Token] = token
        self.params: list[Node] = []

    def append(self, node: Self) -> None:
        self.params.append(node)

    def __repr__(self) -> str:
        return f"<Node: '{str(self.token)}' [{', '.join(list(map(str, self.params)))}]>"
