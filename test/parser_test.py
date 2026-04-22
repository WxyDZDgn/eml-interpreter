from exer.parser import parser

import pytest
from typing import Optional


@pytest.mark.parametrize(
    "code, error",
    [
        ("h() == 1;", "期望标识符或常数"),
        ("h() = = 1;", "期望标识符或常数"),
        ("h() = 1 = 1;", None), # 语法允许, 语义不允许（类型推断错误）
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
def test_parser_syntax_error_caused_by_assignments(code: str, error: Optional[str]):
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
def test_parser_syntax_error_caused_by_unfinished_stmt(code: str, error: Optional[str]):
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
def test_parser_syntax_error_overall(code: str, error: bool):
    if error:
        with pytest.raises(SyntaxError):
            parser(code)
    else:
        parser(code)

if __name__ == "__main__":
    code = """e(x) = eml(x, 1)
            ln(x) = eml(1, eml(eml(1, x), 1));"""
    parser(code)
    """e(x) = eml(x, 1) // ??==;-=+???  cds
            ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????"""
