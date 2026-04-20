from exer.parser import parser, _next_ignore_whitespaces_and_annotations
from exer.lexer import lexer

import pytest
from typing import Optional


@pytest.mark.parametrize(
    "code, error",
    [
        ("h() == 1;", "同一个语句中不支持多个'='"),
        ("h() = = 1;", "同一个语句中不支持多个'='"),
        ("h() = 1;", None),
        (
            """e(x) == eml(x, 1);
            ln(x) = eml(1, eml(eml(1, x), 1));""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1);
            ln(x) == eml(1, eml(eml(1, x), 1));""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1);
            ln(x) = eml(1, eml(eml(1, x), 1));""",
            None,
        ),
        (
            """e(x) == eml(x, 1); // ==-+=++;==?????
            ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1);  // ==-+=++;==?????
            ln(x) == eml(1, eml(eml(1, x), 1));// ??==;-=+???  cds""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1);  // ==-+=++;==?????
            ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""",
            None,
        ),
    ],
)
def test_parser_error_caused_by_assignments(code: str, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            parser(code)
    else:
        parser(code)


@pytest.mark.parametrize(
    "code, error",
    [
        ("h() = 1", "未完成的Stmt"),
        ("h() = 1;", None),
        (
            """e(x) = eml(x, 1)
            ln(x) = eml(1, eml(eml(1, x), 1));""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1);
            ln(x) = eml(1, eml(eml(1, x), 1))""",
            "未完成的Stmt",
        ),
        (
            """e(x) = eml(x, 1);
            ln(x) = eml(1, eml(eml(1, x), 1));""",
            None,
        ),
        (
            """e(x) = eml(x, 1) // ??==;-=+???  cds
            ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????""",
            "同一个语句中不支持多个'='",
        ),
        (
            """e(x) = eml(x, 1); // ??==;-=+???  cds
            ln(x) = eml(1, eml(eml(1, x), 1)) // ==-+=++;==?????""",
            "未完成的Stmt",
        ),
        (
            """e(x) = eml(x, 1); // ??==;-=+???  cds
            ln(x) = eml(1, eml(eml(1, x), 1)); // ==-+=++;==?????""",
            None,
        ),
    ],
)
def test_parser_error_caused_by_unfinished_stmt(code: str, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            parser(code)
    else:
        parser(code)


@pytest.mark.parametrize(
    "code, error",
    [
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
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g);", False),

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
        ("f() = f(1, f(2, 3), f(4, 5, 6), f, g);", False),
    ],
)
def test_parser_error_overall(code: str, error: bool):
    if error:
        with pytest.raises(SyntaxError):
            parser(code)
    else:
        parser(code)


if __name__ == "__main__":
    code = "f() = f(1, f(2, 3), f(4, 5, 6), f, g);"
    for i in range(1, len(code) + 1):
        print(code[:i])
