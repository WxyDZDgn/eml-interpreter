from exer.lexer import lexer

text = """
ex(x) = eml(x, 1);
ln(x) = eml(1, ex(eml(1, x)));
// 测试
"""

if __name__ == '__main__':
    print(lexer(text))
