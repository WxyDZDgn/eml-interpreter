# @Time : 2026/6/14 08:51
# @Author : Whania
# @FileName: parser_test_run.py
from exer.parser import parser

if __name__ == "__main__":
    code = """e(x) = eml(x, 1) ;// ??==;-=+???  cds
            ln(x) = eml(1, eml(eml(1, x), 1));  // ==-+=++;==?????"""
    print(parser(code))

"""
e(x) = eml(x, 1);
ln(x) = eml(1, eml(eml(1, x), 1));

[
    <Node: '<Assignment: '='>' [
        <Node: '<IdentVariable: 'e'>' [
            <Node: '<IdentVariable: 'x'>' [
            ]>
        ]>, 
        <Node: '<IdentVariable: 'eml'>' [
            <Node: '<IdentVariable: 'x'>' [
            ]>, 
            <Node: '<ConstInt: '1'>' [
            ]>
        ]>
    ]>, 
    <Node: '<Assignment: '='>' [
        <Node: '<IdentVariable: 'ln'>' [
            <Node: '<IdentVariable: 'x'>' [
            ]>
        ]>, 
        <Node: '<IdentVariable: 'eml'>' [
            <Node: '<IdentVariable: 'eml'>' [
                <Node: '<IdentVariable: 'eml'>' [
                    <Node: '<ConstInt: '1'>' [
                    ]>, 
                    <Node: '<IdentVariable: 'x'>' [
                    ]>
                ]>, 
                <Node: '<IdentVariable: 'eml'>' [
                ]>, 
                <Node: '<ConstInt: '1'>' [
                ]>
            ]>, 
            <Node: '<ConstInt: '1'>' [
            ]>, 
            <Node: '<IdentVariable: 'eml'>' [
            ]>
        ]>
    ]>
]
"""
