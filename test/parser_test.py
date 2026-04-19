from exer.parser import Parser

import pytest
from typing import Optional


@pytest.mark.parametrize(
    "code, error", [
        ("h == 1;", "同一个语句中不支持多个'='"), 
        ("h = = 1;", "同一个语句中不支持多个'='"), 
        ("h = 1;", None),
        ("""e(x) == eml(x, 1);
         ln(x) = eml(1, eml(eml(1, x), 1));""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1);
         ln(x) == eml(1, eml(eml(1, x), 1));""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1);
         ln(x) = eml(1, eml(eml(1, x), 1));""", None),
        ("""e(x) == eml(x, 1); // ==-+=++;==?????
         ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1);  // ==-+=++;==?????
         ln(x) == eml(1, eml(eml(1, x), 1));// ??==;-=+???  cds""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1);  // ==-+=++;==?????
         ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""", None),
    ]
)
def test_parser_error_caused_by_assignments(code: str, error: Optional[str]):
    if error is not None:
        with pytest.raises(AssertionError, match=error):
            p = Parser()
            p.exec(code)
    else:
        p = Parser()
        p.exec(code)

@pytest.mark.parametrize(
    "code, error", [
        ("h = 1", "未完成的Stmt"), 
        ("h = 1;", None),
        ("""e(x) = eml(x, 1)
         ln(x) = eml(1, eml(eml(1, x), 1));""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1);
         ln(x) = eml(1, eml(eml(1, x), 1))""", "未完成的Stmt"),
        ("""e(x) = eml(x, 1);
         ln(x) = eml(1, eml(eml(1, x), 1));""", None),
        ("""e(x) = eml(x, 1) // ??==;-=+???  cds
         ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????""", "同一个语句中不支持多个'='"),
        ("""e(x) = eml(x, 1); // ??==;-=+???  cds
         ln(x) = eml(1, eml(eml(1, x), 1)) // ==-+=++;==?????""", "未完成的Stmt"),
        ("""e(x) = eml(x, 1); // ??==;-=+???  cds
         ln(x) = eml(1, eml(eml(1, x), 1)); // ==-+=++;==?????""", None),
    ]
)
def test_parser_error_caused_by_unfinished_stmt(code: str, error: Optional[str]):
    if error is not None:
        with pytest.raises(AssertionError, match=error):
            p = Parser()
            p.exec(code)
    else:
        p = Parser()
        p.exec(code)

if __name__ == '__main__':
    p = Parser()
    p.exec("""e(x) == eml(x, 1); // ==-+=++;==?????
         ln(x) = eml(1, eml(eml(1, x), 1)); // ??==;-=+???  cds""")
    