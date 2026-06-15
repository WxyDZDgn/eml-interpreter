# @Time : 2026/6/14 11:30
# @Author : Whania
# @FileName: semantic_analyzer_test_run.py
from exer.semantic_analyzer import semantic_analyzer

if __name__ == '__main__':
    code = """e(x) = eml(x, 1) ;// ??==;-=+???  cds
                ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????"""
    print(semantic_analyzer(code))

"""
e(x) = eml(x, 1) ;// ??==;-=+???  cds
                ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????


"""