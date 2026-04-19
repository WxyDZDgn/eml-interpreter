from exer.parser import parser

import pytest
from typing import Optional


@pytest.mark.parametrize(
    "code, error",
    [
        ("h == 1;", "同一个语句中不支持多个'='"),
        ("h = = 1;", "同一个语句中不支持多个'='"),
        ("h = 1;", None),
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
        ("h = 1", "未完成的Stmt"),
        ("h = 1;", None),
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


if __name__ == "__main__":
    parser(
        "eml(x)  = eml(x, y);"
    )
