import re
from typing import Any


def build_lambda_head(argv_size: int, args_as_list: bool = False) -> str:
    if args_as_list:
        return ""
    lmbd = "lambda "
    for idx in range(argv_size):
        lmbd += f"_arg{idx}"
        if idx != argv_size - 1:
            lmbd += ","
    lmbd += ":"
    return lmbd


def build_lambda_body(expr: str, argv_size: int, args_as_list: bool = False) -> str:
    if args_as_list:
        expr = re.sub(r"\$i", "y", expr)
        expr = re.sub(r"\$@", "argv", expr)
        return f"[{expr}]"
    else:
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
