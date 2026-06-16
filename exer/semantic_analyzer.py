from exer.parser import parser
from unit.expected_state import ExpectedState
from unit.node import Node
from unit.symbol_table import SymbolTable
from unit.token import Execute, Assignment, IdentVariable, FunctionVariable, ParameterVariable, ConstInt
from unit.eml_syntax_error import raise_syntax_error


def _semantic_construct_node(root: Node, is_after_assignment: bool, is_first_layer: bool,
                             symbol_tables: list[SymbolTable]) -> Node:
    assert len(symbol_tables) >= 1
    if is_after_assignment:
        if isinstance(root.token, IdentVariable):
            symbol_table_index = len(symbol_tables) - 1
            while symbol_table_index >= 0:
                if root in symbol_tables[symbol_table_index]:
                    break
                symbol_table_index -= 1
            if symbol_table_index < 0:
                assert root.token is not None
                raise_syntax_error(ExpectedState.DEFINED_STATE, root.token)
                assert False
            cur_table = symbol_tables[symbol_table_index]
            src_token = cur_table.get_recycle(root.token, len(root.params))
            assert src_token is not None
            if isinstance(src_token, FunctionVariable):
                root.token = FunctionVariable(root.token)
            elif isinstance(src_token, ParameterVariable):
                root.token = ParameterVariable(root.token)
            else:
                assert False
    else:
        if isinstance(root.token, ConstInt):
            assert len(root.params) <= 0
            if is_first_layer:
                raise_syntax_error(ExpectedState.FUNCTION_STATE, root.token)
                assert False
            raise_syntax_error(ExpectedState.PARAMETER_STATE, root.token)
            assert False
        if isinstance(root.token, IdentVariable):
            if not is_first_layer and len(root.params) > 0:
                raise_syntax_error(ExpectedState.PARAMETER_STATE, root.token)
                assert False
            if is_first_layer:
                root.token = FunctionVariable(root.token)
            else:
                root.token = ParameterVariable(root.token)
                assert root.token is not None
                assert len(root.params) <= 0
                cur_table = symbol_tables[-1]
                if cur_table.is_defined(root.token, len(root.params)):
                    raise_syntax_error(ExpectedState.UNIQUE_PARAM_STATE, root.token)
                    assert False
                _ = cur_table.put(root.token, len(root.params))
                assert _

    for n_index in range(len(root.params)):
        root.params[n_index] = _semantic_construct_node(root.params[n_index], is_after_assignment, False, symbol_tables)

    return root


def semantic_analyzer(code: str) -> Node:
    """
        语义分析器，根据 AST 节点列表整合成一个 AST，对节点进行专有优化，并同时检查语义错误

        参数:
            code: 代码片段

        返回:
            Node: AST 根节点
        """
    nodes = parser(code)
    root = Node(Execute())
    symbol_tables: list[SymbolTable] = [SymbolTable()]

    symbol_tables[0].put(FunctionVariable(IdentVariable("eml")), 2)

    for node in nodes:
        # 在这里检查语义
        if isinstance(node.token, Assignment):
            assert len(node.params) == 2
            symbol_tables.append(SymbolTable())

            node.params[0] = _semantic_construct_node(node.params[0], False, True, symbol_tables)
            node.params[1] = _semantic_construct_node(node.params[1], True, True, symbol_tables)

            symbol_tables.pop()
            root_table = symbol_tables[0]
            assert node.params[0].token is not None
            _ = root_table.put(node.params[0].token, len(node.params[0].params))
            assert _
        else:
            node = _semantic_construct_node(node, True, True, symbol_tables)
        root.append(node)
    return root
