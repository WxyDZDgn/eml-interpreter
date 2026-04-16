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
    ]
    ls = map(str, ls)
    print('\n'.join(ls))
