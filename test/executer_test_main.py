# @Time : 2026/6/17 07:40
# @Author : Whania
# @FileName: executer_test_main.py
from exer.executer import Executer

if __name__ == '__main__':
    ex = Executer()
    ex.exec("f(x) = eml(1, 2);")
    ex.exec("g(x) = eml(x, 2);")
    ex.exec("h(x) = g(x);")
    ex.exec("i(x) = g(x, 1);")
