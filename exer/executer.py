from typing import Optional

from exer.semantic_analyzer import SemanticAnalyzer
from unit.node import Node
from unit.token import Execute, ParameterVariable, FunctionVariable, Assignment
import traceback

from unit.symbol_table import SymbolTable


class Executer:
    def __init__(self) -> None:
        self.symbol_table: SymbolTable = SymbolTable()
        self.semantic_analyzer: SemanticAnalyzer = SemanticAnalyzer()
        pass

    def _recursive_exec(self, root: Node, parameters_definition: Optional[Node] = None) -> None:
        assert parameters_definition is None or isinstance(parameters_definition.token, FunctionVariable)

        pass

    def exec(self, code: str) -> None:
        # noinspection PyBroadException
        try:
            ast_node = self.semantic_analyzer.analyze(code)
            assert isinstance(ast_node.token, Execute)

            for node in ast_node.params:
                if isinstance(node.token, Assignment):
                    assert len(node.params) == 2
                    def_node, exec_node = node.params[0], node.params[1]
                    assert isinstance(def_node.token, FunctionVariable)
                    self._recursive_exec(exec_node, def_node)
                    self.symbol_table.put(def_node.token, len(def_node.params), ast_node=node)
                else:
                    self._recursive_exec(node)
            pass
        except SyntaxError:
            traceback.print_exc(limit=0)
            exit(1)
        except AssertionError:
            assert False
