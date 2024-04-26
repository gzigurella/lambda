from argparse import ArgumentParser, RawTextHelpFormatter, FileType, Namespace
from datetime import datetime
from os import strerror
from re import findall
from sys import argv as sys_argv, stdout, stdin
from traceback import print_exc
from functools import reduce
from pydoc import locate
from typing import Any, TextIO

from src.constants import LIST_SPECIAL_ARG, SCRIPT_SPECIAL_ARG, EXPR_ARGS_REGEX, EXPR_ARGS_INDICATOR, STRING_BLANK, \
    VERSION, ERRNO
from src.evaluator import build_lambda_head, build_lambda_body, build_lambda_args


def get_current_year():
    return datetime.now().year.real


parser = ArgumentParser(
    prog='lambda',
    description='''description:
    Execute python lambda's body expression on positional arguments or 
    operations on file with arrays and list comprehension.

    Example on positional arguments: lambda \"#1 ** #2\" arg1 arg2
    Example on list arguments: lambda \"#i + 2 for #i in #?\" arg1 arg2 ... argN
    Example of reduction: lambda -r 0 -dt=int \"#1+#2\" arg1 arg2 ... argN
    Example of execution of external lambda script: lambda #script::/absolute/path/to/script.lambda arg1 arg2 ... argN
    ''',
    formatter_class=RawTextHelpFormatter,
    epilog=f'Author: Gabriele Zigurella © {get_current_year()}')

parser.add_argument('expr', metavar='EXPR', type=str, nargs=1,
                    help='Lambda expression or list comprehension expression to be applied')
parser.add_argument('args', metavar='@A', type=str, nargs='*',
                    help='Positional Arguments to be used during the lambda invocation')
parser.add_argument('-r', '--reduce=', dest='reduce', action='store',
                    nargs='?',
                    help='If enabled it will apply to the given accumulator the lambda with the positional values')
parser.add_argument('-D', '--debug', dest='debug', action='store_true',
                    help='It will output traceback errors on execution failure.')
parser.add_argument('-dt', '--dtype=', dest='dtype', action='store',
                    default='str', nargs=1,
                    help='Define the type of the positional arguments, if omitted they will be treated as strings.')
parser.add_argument('-f', '--filepath=', dest='source', type=FileType('r'),
                    nargs='?', default=stdin,
                    help='Define the File from witch to read, each lines will be parsed into a list argument.')
parser.add_argument('-d', '--delim=', dest='delimiter', type=str, nargs='?',
                    help='''Combined with flag -f (or --filepath) allows to split each file line on given delimiter
                         and treat each split value as an argument.''')
parser.add_argument('-o', '--output=', dest='output', type=FileType('w'),
                    nargs='?', default=stdout,
                    help='Define the File to write at the end of the operation.')
parser.add_argument('-v', '--version=', dest='version', action='store_true',
                    default=False,
                    help='Output current program version')


def search_number_of_lambda_args(expr: str) -> int:
    return [int(match.replace(EXPR_ARGS_INDICATOR, STRING_BLANK)) for match in findall(EXPR_ARGS_REGEX, expr)][-1]


def exec_script(options: Namespace) -> Any:
    """
    Executes all lambda function defined inside a *.lambda file script, line by line.

    :param options: the parsed arguments and options from the program invocation
    :return: The result of the application of all the lambda functions described in the file script
    """
    expr = options.expr[0]
    with open(expr.replace(SCRIPT_SPECIAL_ARG, STRING_BLANK)) as script:
        expressions = [expr.strip() for expr in script.readlines()]
        for idx, expr in enumerate(expressions):
            options.expr = [expr]
            if idx == len(expressions) - 1:
                return exec_lambda(options)
            # carry the last expression result as argument for the next one
            options.args = [exec_lambda(options)]
            # reset reduction initial value
            options.reduce = None
            # reset data type based on result
            options.dtype = [type(options.args[0]).__name__]


def exec_list_comprehension_lambda(expr: str, argv: list[Any]):
    """
    The eval searches the closest reference to 'argv' therefore finding the one in the function scope, and applies the
    expression to each element of the list.
    :param expr: The List Comprehension Expression to apply
    :param argv: The List onto apply the function
    :return:
    """
    list_comprehension = build_lambda_body(expr, None, True)
    return eval(list_comprehension)


def exec_lambda_func(expr: str, argv: list[Any], reduce_initial_value: Any | None):
    """
    The eval searches the closest reference to 'argv' therefore finding the one in the function scope,
    and tries to apply the lambda expression to the elements from argv list.
    Any exceeding argument is discarded.
    :param expr: the expression of the lambda function
    :param argv: the vector of the positional arguments
    :param reduce_initial_value: the (optional) initial value of the Reduction
    :return: the result of the applied lambda on the argv list
    """
    n_of_args = search_number_of_lambda_args(expr)
    __lambda__ = eval(
        build_lambda_head(n_of_args, False)
        +
        build_lambda_body(expr, n_of_args, False)
    )
    if reduce_initial_value is not None:
        return reduce(__lambda__, argv, reduce_initial_value)
    else:
        __args__ = build_lambda_args(argv, len(argv))
        return __lambda__(*argv[:n_of_args])


def exec_lambda(options: Namespace) -> Any:
    """
    The Program decision Behaviour function,
    it chooses between the lambda function evaluation and the list comprehension one.
    :param options: The list of arguments and options parsed from the program invocation
    :return: the result of the applied expressions parsed from the system arguments vector
    """
    res: Any
    # Get Lambda Expression
    __lambda_expr__ = options.expr[0]
    # Parse arguments vector
    argv = lambda_input(options)
    if LIST_SPECIAL_ARG not in __lambda_expr__:
        res = exec_lambda_func(__lambda_expr__, argv, options.reduce)
    else:
        res = exec_list_comprehension_lambda(__lambda_expr__, argv)
    return res


def main(argv: list[str]) -> (int, str):
    __program__ = argv[0]
    __args__ = argv[1:]
    # If we receive the version flag skip the rest of the program
    if version(__args__):
        return 0
    options = parser.parse_args(__args__)
    if options.debug:
        print(f"### PARSED OPTIONS AND ARGUMENTS\n\n{options}\n\n###")
    try:
        __lambda_expr__ = options.expr[0]
        res: Any = None
        if SCRIPT_SPECIAL_ARG in __lambda_expr__:
            res = exec_script(options)
        else:
            res = exec_lambda(options)
        output(res, options.output)
    except (ValueError, TypeError):
        if options.debug:
            print_exc()
        return ERRNO['Invalid Argument'], "Either wrong argument type or missing a --dtype flag."
    except RuntimeError:
        if options.debug:
            print_exc()
        return ERRNO['Generic Error'], "An unknown error occurred during the execution, please re-run it with -D flag enabled to see what's wrong."
    return 0, None


def lambda_input(options: Namespace):
    args: Any
    if options.source != stdin:
        with open(options.source.name) as file:
            options.args = [line.strip() for line in file]
            if options.delimiter is not None:
                def flatten_concatenation(arg_matrix):
                    flat_list = []
                    for row in arg_matrix:
                        flat_list += row.split(options.delimiter)
                    return flat_list

                options.args = flatten_concatenation(options.args)
    if options.dtype == 'str':
        args = options.args
    else:
        dtype: object = locate(options.dtype[0])
        args = [dtype(arg) for arg in options.args]
        if options.reduce is not None:
            options.reduce = dtype(options.reduce)
    return args


def output(res: Any, out: TextIO):
    echo = f"{res}"
    if isinstance(res, list):
        echo = "\n".join([val.strip() for val in f"{res}".replace('[', STRING_BLANK).replace(']', STRING_BLANK).split(',')])
    if out == stdout:
        print(echo)
    else:
        with open(out.name, 'w') as file:
            file.write(echo)


def version(args: list[str]) -> bool:
    if '-v' in args or '--version' in args:
        print(VERSION)
        return True
    return False


if __name__ == '__main__':
    exit_code, message = main(sys_argv)
    if exit_code != 0:
        print(strerror(exit_code), message)
