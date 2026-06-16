# @Time : 2026/6/16 11:44
# @Author : Whania
# @FileName: semantic_analyzer_test.py
from typing import Optional

import pytest

from exer.semantic_analyzer import semantic_analyzer


@pytest.mark.parametrize(
    "code, error",
    [
        ("e() = 1;", None),
        ("e(x) = 1;", None),
        ("e(x()) = 1;", None),
        ("e(x(a)) = 1;", "期望参数标识符"),
        ("e(x(a())) = 1;", "期望参数标识符"),
        ("e(x(a(b))) = 1;", "期望参数标识符"),
        ("1 = eml(x, 1);", "期望函数标识符"),
        ("f(a(), b, 1) = eml(x, 1);", "期望参数标识符"),
        ("f(a(), b, a) = eml(x, 1);", "非重复参数标识符"),
        ("f(a(), 2, a) = eml(x, 1);", "期望参数标识符"),
    ],
)
def test_semantic_syntax_before_assignment_error(code, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            semantic_analyzer(code)
    else:
        semantic_analyzer(code)
