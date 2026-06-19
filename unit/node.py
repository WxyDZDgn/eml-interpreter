from unit.token import Token

from typing import Self, Optional
from copy import deepcopy


class Node:
    def __init__(self, token: Optional[Token] = None) -> None:
        self.token: Optional[Token] = token
        self.params: list[Node] = []

    def append(self, node: Self) -> None:
        self.params.append(node)

    def __repr__(self) -> str:
        return f"<Node: '{str(self.token)}' [{', '.join(list(map(str, self.params)))}]>"

    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]
        root = type(self)(self.token)
        memo[id(root)] = root
        for p in self.params:
            root.params.append(deepcopy(p, memo))
        return root
