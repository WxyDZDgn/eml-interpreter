# @Time : 2026/6/14 08:51
# @Author : Whania
# @FileName: parser_test_run.py
from exer.parser import parser

if __name__ == "__main__":
    code = """e(x) = eml(x, 1);
ln(x) = eml(1, eml(eml(1, x), 1));"""
    nodes = parser(code)
    print(nodes)
