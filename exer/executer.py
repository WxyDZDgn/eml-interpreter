from exer.semantic_analyzer import SemanticAnalyzer
from unit.token import Execute
import traceback

from unit.symbol_table import SymbolTable


class Executer:
    def __init__(self) -> None:
        self.symbol_table: SymbolTable = SymbolTable()
        self.semantic_analyzer: SemanticAnalyzer = SemanticAnalyzer()
        pass

    def exec(self, code: str) -> None:
        # noinspection PyBroadException
        try:
            ast_node = self.semantic_analyzer.analyze(code)
            assert isinstance(ast_node.token, Execute)
            pass
        except SyntaxError:
            traceback.print_exc(limit=0)
            exit(1)
        except AssertionError:
            assert False
