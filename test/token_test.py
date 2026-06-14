from unit.token import *

if __name__ == '__main__':
    ls = [
        FuncEml(),
        OpenParen(),
        CloseParen(),
        Comma(),
        ConstInt(20),
        EndOfStmt(),
        IdentVariable("eml"),
        WhiteSpace("   \t   \t   "),
        Assignment(),
        Unknown("?????"),
        Annotation("//urdsnvfsd"),
        ParameterVariable(IdentVariable("x")),
        FunctionVariable(IdentVariable("f")),
    ]
    ls = map(str, ls)
    print('\n'.join(ls))
