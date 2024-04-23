import os, re, sys
from typing import Any


def build_lambda_head(argv_size: int) -> str:
    lmbd = "lambda "
    for idx in range(argv_size):
        lmbd += f"_arg{idx}"
        if idx != argv_size - 1:
            lmbd += ","
    lmbd += ":"
    return lmbd


def build_lambda_body(expr: str, argv_size: int) -> str:
    for idx in range(argv_size):
        replaced_arg = f"\\${idx + 1}"
        replace_value = f"_arg{idx}"
        expr = re.sub(replaced_arg, replace_value, expr)
    return expr


def build_lambda_args(argv: list[Any], argv_size: int) -> str:
    lmbd = "("
    for idx in range(argv_size):
        lmbd += f"{argv[idx]}"
        if idx != argv_size - 1:
            lmbd += ","
    lmbd += ")"
    return lmbd


def main(expr: str, argv: list[Any]) -> int:
    try:
        argv_size = len(argv)
        __lambda__ = eval(build_lambda_head(argv_size) + build_lambda_body(expr, argv_size))
        __args__ = build_lambda_args(argv, argv_size)
        res = __lambda__(*argv)
        print(res)
    except Exception as e:
        print(e)
        print(os.strerror(32))
        return 32
    return 0


def usage():
    print(f"""
    > lambda \"$1 ** $2\" arg1 arg2
    > lambda \"k + 2 for k in $@\" arg1...argN
    
    ### OPTIONAL FLAGS ###
        -h, --help | show this usage message for guidance
        
    ### LAMBDA ARGUMENTS ###
    Lambda uses positional arguments $1, $2, $N to evaluate and apply the python expression on the given input.
    If not explicit cast is given all lambda parameters are tought to be string type.
    
    Use $@ to apply the lambda to all given parameters, considering them part of an Array of elements.
    """)


if __name__ == '__main__':
    if "-h" in sys.argv or "--help" in sys.argv:
        usage()
        exit(0)
    if len(sys.argv) < 2:
        print("INVALID ARGUMENTS ERROR: Please invoke 'lambda -h' or 'lambda --help' to see the correct program usage.")
    __program__ = sys.argv[0]
    __lambda_expr__ = sys.argv[1]
    __lamda_args__ = sys.argv[2:]
    exit(main(__lambda_expr__, __lamda_args__))
