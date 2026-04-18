from exer.parse import Parser

if __name__ == '__main__':
    p = Parser()
    code = """
ex(x) = eml(x, 1);
ln(x) = eml(1, ex(eml(1, x)));
"""
    p.exec(code)
    pass
