# @Time : 2026/6/16 11:44
# @Author : Whania
# @FileName: semantic_analyzer_test.py
from typing import Optional

import pytest

from exer.semantic_analyzer import SemanticAnalyzer


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
            SemanticAnalyzer().analyze(code)
    else:
        SemanticAnalyzer().analyze(code)


@pytest.mark.parametrize(
    "code, error",
    [
        ("f(a(), b, c) = eml(x, 1);", "期望已定义标识符"),
        ("f(a(), b, c) = eml(a, 1);", None),
        ("f(a(), b, c) = eml(c, 1); g(h, f) = f(2, h, i);", "期望已定义标识符"),
        ("f(a(), b, c) = eml(c, 1); g(h, i) = f(2, h, i);", None),
        ("eml(x, y) = eml(x, y);", None),
        ("eml(x, y, z) = eml(x, y, z);", "期望已定义标识符"),
        ("f(x, y) = eml(x, y); g(x, y) = f(1, x, y);", "期望已定义标识符"),
        ("f(x, y) = eml(x, y); g(x, y) = f(1, x);", None),
        ("f(x, y) = eml(x, y); g(x, y) = f(x);", "期望已定义标识符"),
        ("eml(x, y);", "期望已定义标识符"),
        ("eml(x, 1);", "期望已定义标识符"),
        ("eml(2, y);", "期望已定义标识符"),
        ("eml(2, y);", "期望已定义标识符"),
        ("eml(2, 1);", None),
        ("eml(2);", "期望已定义标识符"),
        ("eml();", "期望已定义标识符"),
        ("eml(1, 2, 3);", "期望已定义标识符"),
    ],
)
def test_semantic_syntax_after_assignment_error(code, error: Optional[str]):
    if error is not None:
        with pytest.raises(SyntaxError, match=error):
            SemanticAnalyzer().analyze(code)
    else:
        SemanticAnalyzer().analyze(code)
