from exer.parser import parser

import pytest
import re
from typing import Optional


@pytest.mark.parametrize(
    "code, error",
    [
        ("h() == 1;", "期望标识符或常数"),
        ("h() = = 1;", "期望标识符或常数"),
        ("h() = 1 = 1;", None),  # 语法允许, 语义不允许（类型推断错误）
        ("h() = 1;", None),
        (
                """e(x) == eml(x, 1);
                ln(x) = eml(1, eml(eml(1, x), 1));""",
                "期望标识符或常数",
        ),
        (
                """e(x) = eml(x, 1);
                ln(x) == eml(1, eml(eml(1, x), 1));""",
                "期望标识符或常数",
        ),
        (
                """e(x) = eml(x, 1);
                ln(x) = eml(1, eml(eml(1, x), 1));""",
                None,
        ),
        (
                """e(x) == eml(x, 1); // ==-+=++;==?????
                ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""",
                "期望标识符或常数",
        ),
        (
                """e(x) = eml(x, 1);  // ==-+=++;==?????
                ln(x) == eml(1, eml(eml(1, x), 1));// ??==;-=+???  cds""",
                "期望标识符或常数",
        ),
        (
                """e(x) = eml(x, 1);  // ==-+=++;==?????
                ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""",
                None,
        ),
    ],
)
def test_parser_syntax_error_caused_by_assignments(code, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            parser(code)
    else:
        parser(code)


@pytest.mark.parametrize(
    "code, error",
    [
        ("h() = 1", "期望';'"),
        ("h() = 1;", None),
        (
                """e(x) = eml(x, 1)
                ln(x) = eml(1, eml(eml(1, x), 1));""",
                "期望';'",
        ),
        (
                """e(x) = eml(x, 1);
                ln(x) = eml(1, eml(eml(1, x), 1))""",
                "期望';'",
        ),
        (
                """e(x) = eml(x, 1);
                ln(x) = eml(1, eml(eml(1, x), 1));""",
                None,
        ),
        (
                """e(x) = eml(x, 1) // ??==;-=+???  cds
                ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????""",
                "期望';'",
        ),
        (
                """e(x) = eml(x, 1); // ??==;-=+???  cds
                ln(x) = eml(1, eml(eml(1, x), 1)) // ==-+=++;==?????""",
                "期望';'",
        ),
        (
                """e(x) = eml(x, 1); // ??==;-=+???  cds
                ln(x) = eml(1, eml(eml(1, x), 1)); // ==-+=++;==?????""",
                None,
        ),
    ],
)
def test_parser_syntax_error_caused_by_unfinished_stmt(code, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            parser(code)
    else:
        parser(code)


@pytest.mark.parametrize(
    "code, error",
    [
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g);", False),

        ("f", True),
        ("f(", True),
        ("f()", True),
        ("f() ", True),
        ("f() =", True),
        ("f() = ", True),
        ("f() = f", True),
        ("f() = f(", True),
        ("f() = f(1", True),
        ("f() = f(1,", True),
        ("f() = f(1, ", True),
        ("f() = f(1, f", True),
        ("f() = f(1, f(", True),
        ("f() = f(1, f(2", True),
        ("f() = f(1, f(2,", True),
        ("f() = f(1, f(2, ", True),
        ("f() = f(1, f(2, 3", True),
        ("f() = f(1, f(2, 3)", True),
        ("f() = f(1, f(2, 3),", True),
        ("f() = f(1, f(2, 3), ", True),
        ("f() = f(1, f(2, 3), f", True),
        ("f() = f(1, f(2, 3), f(", True),
        ("f() = f(1, f(2, 3), f(4", True),
        ("f() = f(1, f(2, 3), f(4,", True),
        ("f() = f(1, f(2, 3), f(4, ", True),
        ("f() = f(1, f(2, 3), f(4, 5", True),
        ("f() = f(1, f(2, 3), f(4, 5,", True),
        ("f() = f(1, f(2, 3), f(4, 5, ", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6)", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6),", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), ", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f,", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, ", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g)", True),

        ("f;", False),
        ("f(;", True),
        ("f();", False),
        ("f() ;", False),
        ("f() =;", True),
        ("f() = ;", True),
        ("f() = f;", False),
        ("f() = f(;", True),
        ("f() = f(1;", True),
        ("f() = f(1,;", True),
        ("f() = f(1, ;", True),
        ("f() = f(1, f;", True),
        ("f() = f(1, f(;", True),
        ("f() = f(1, f(2;", True),
        ("f() = f(1, f(2,;", True),
        ("f() = f(1, f(2, ;", True),
        ("f() = f(1, f(2, 3;", True),
        ("f() = f(1, f(2, 3);", True),
        ("f() = f(1, f(2, 3),;", True),
        ("f() = f(1, f(2, 3), ;", True),
        ("f() = f(1, f(2, 3), f;", True),
        ("f() = f(1, f(2, 3), f(;", True),
        ("f() = f(1, f(2, 3), f(4;", True),
        ("f() = f(1, f(2, 3), f(4,;", True),
        ("f() = f(1, f(2, 3), f(4, ;", True),
        ("f() = f(1, f(2, 3), f(4, 5;", True),
        ("f() = f(1, f(2, 3), f(4, 5,;", True),
        ("f() = f(1, f(2, 3), f(4, 5, ;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6);", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6),;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), ;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f,;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, ;", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g;", True),

        ("f);", True),
        ("f();", False),
        ("f());", True),
        ("f() );", True),
        ("f() =);", True),
        ("f() = );", True),
        ("f() = f);", True),
        ("f() = f();", False),
        ("f() = f(1);", False),
        ("f() = f(1,);", True),
        ("f() = f(1, );", True),
        ("f() = f(1, f);", False),
        ("f() = f(1, f();", True),
        ("f() = f(1, f(2);", True),
        ("f() = f(1, f(2,);", True),
        ("f() = f(1, f(2, );", True),
        ("f() = f(1, f(2, 3);", True),
        ("f() = f(1, f(2, 3));", False),
        ("f() = f(1, f(2, 3),);", True),
        ("f() = f(1, f(2, 3), );", True),
        ("f() = f(1, f(2, 3), f);", False),
        ("f() = f(1, f(2, 3), f();", True),
        ("f() = f(1, f(2, 3), f(4);", True),
        ("f() = f(1, f(2, 3), f(4,);", True),
        ("f() = f(1, f(2, 3), f(4, );", True),
        ("f() = f(1, f(2, 3), f(4, 5);", True),
        ("f() = f(1, f(2, 3), f(4, 5,);", True),
        ("f() = f(1, f(2, 3), f(4, 5, );", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6);", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6));", False),
        ("f() = f(1, f(2, 3), f(4, 5, 6),);", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), );", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f);", False),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f,);", True),
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, );", True),

        (") = f() ;", True),
        (" ) = f() ;", True),
        (" f) = f() ;", True),
        (" f() = f() ;", False),
        (" f(1) = f() ;", False),
        (" f(1,) = f() ;", True),
        (" f(1, ) = f() ;", True),
        (" f(1, f) = f() ;", False),
        (" f(1, f() = f() ;", True),
        (" f(1, f(2) = f() ;", True),
        (" f(1, f(2,) = f() ;", True),
        (" f(1, f(2, ) = f() ;", True),
        (" f(1, f(2, 3) = f() ;", True),
        (" f(1, f(2, 3)) = f() ;", False),
        (" f(1, f(2, 3),) = f() ;", True),
        (" f(1, f(2, 3), ) = f() ;", True),
        (" f(1, f(2, 3), f) = f() ;", False),
        (" f(1, f(2, 3), f() = f() ;", True),
        (" f(1, f(2, 3), f(4) = f() ;", True),
        (" f(1, f(2, 3), f(4,) = f() ;", True),
        (" f(1, f(2, 3), f(4, ) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5,) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, ) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, 6) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, 6)) = f() ;", False),
        (" f(1, f(2, 3), f(4, 5, 6),) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, 6), ) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, 6), f) = f() ;", False),
        (" f(1, f(2, 3), f(4, 5, 6), f,) = f() ;", True),
        (" f(1, f(2, 3), f(4, 5, 6), f, ) = f() ;", True),
    ],
)
def test_parser_syntax_error_overall(code, error: bool):
    if error:
        with pytest.raises(SyntaxError):
            parser(code)
    else:
        parser(code)


@pytest.mark.parametrize(
    "code, expected_raw",
    [
        (
                "a(b());",
                "[<Node: '<IdentVariable: 'a'>' [<Node: '<IdentVariable: 'b'>' []>]>]"
        ),
        (
                "1=3;",
                "[<Node: '<Assignment: '='>' [<Node: '<ConstInt: '1'>' []>, <Node: '<ConstInt: '3'>' []>]>]"
        ),
        (
                "a(b())=3;",
                "[<Node: '<Assignment: '='>' [<Node: '<IdentVariable: 'a'>' [<Node: '<IdentVariable: 'b'>' []>]>, <Node: '<ConstInt: '3'>' []>]>]"
        ),
        (
                "a(b(c()));",
                "[<Node: '<IdentVariable: 'a'>' [<Node: '<IdentVariable: 'b'>' [<Node: '<IdentVariable: 'c'>' []>]>]>]"
        )
    ]
)
def test_parser_ast(code, expected_raw):
    def _clear_whitespaces(s: str) -> str:
        return re.sub(r'\s+', '', s)

    actual = str(parser(code))
    assert _clear_whitespaces(actual) == _clear_whitespaces(expected_raw)
