import datetime
import os, sys
import argparse
import re
import traceback
from evaluator import build_lambda_head, build_lambda_body, build_lambda_args
from pydoc import locate
from typing import Any, TextIO
from functools import reduce


def get_current_year():
    return datetime.datetime.now().year.real


parser = argparse.ArgumentParser(
    prog='lambda',
    description='''description:
    Execute python lambda's body expression on positional arguments or 
    operations on file with arrays and list comprehension.

    Example on positional arguments: lambda \"$1 ** $2\" arg1 arg2
    Example on list arguments: lambda \"$i + 2 for $i in $@\" arg1 arg2 ... argN
    Example of reduction: lambda -r 0 -dt=int \"$1+$2\" arg1 arg2 ... argN''',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=f'Author: Gabriele Zigurella © {get_current_year()}')

parser.add_argument('expr', metavar='EXPR', type=str, nargs=1,
                    help='Lambda expression or list comprehension expression to be applied')
parser.add_argument('args', metavar='$A', type=str, nargs='*',
                    help='Positional Arguments to be used during the lambda invocation')
parser.add_argument('-r', '--reduce=', dest='reduce', action='store',
                    nargs='?',
                    help='If enabled it will apply to the given accumulator the lambda with the positional values')
parser.add_argument('-D', '--debug', dest='debug', action='store_true',
                    help='It will output traceback errors on execution failure.')
parser.add_argument('-dt', '--dtype=', dest='dtype', action='store',
                    default='str', nargs=1,
                    help='Define the type of the positional arguments, if omitted they will be treated as strings.')
parser.add_argument('-f', '--filepath=', dest='source', type=argparse.FileType('r'),
                    nargs='?', default=sys.stdin,
                    help='Define the File from witch to read, each lines will be parsed into a list argument.')
parser.add_argument('-d', '--delim=', dest='delimiter', type=str, nargs='?',
                    help='''Combined with flag -f (or --filepath) allows to split each file line on given delimiter
                         and treat each splitted value as an argument.''')
parser.add_argument('-o', '--output=', dest='output', type=argparse.FileType('w'),
                    nargs='?', default=sys.stdout,
                    help='Define the File from witch to read, each lines will be parsed into a list argument.')


def search_number_of_lambda_args(expr: str) -> int:
    return [int(match.replace('$', '')) for match in re.findall(r'\$\d', expr)][-1]


def main(options: argparse.Namespace) -> int:
    try:
        __lambda_expr__ = parsed_cmd.expr[0]
        argv = lambda_input(options)
        res: Any
        argv_size = len(argv)
        if not ("$@" in __lambda_expr__):
            n_of_args = search_number_of_lambda_args(__lambda_expr__)
            __lambda__ = eval(
                build_lambda_head(n_of_args, False) + build_lambda_body(__lambda_expr__, n_of_args, False))
            if options.reduce is not None:
                res = reduce(__lambda__, argv, options.reduce)
            else:
                __args__ = build_lambda_args(argv, argv_size)
                res = __lambda__(*argv)
        else:
            list_comprehension = build_lambda_body(__lambda_expr__, argv_size, True)
            res = eval(list_comprehension)
        output(res, options.output)
    except Exception as e:
        if hasattr(options, 'debug'):
            traceback.print_exc()
        print(os.strerror(32), e)
        return 32
    return 0


def lambda_input(options: argparse.Namespace):
    args: Any
    if options.source != sys.stdin:
        with open(options.source.name) as file:
            options.args = [line.strip() for line in file]
            if hasattr(options, "delimiter"):
                def flatten_concatenation(arg_matrix):
                    flat_list = []
                    for row in arg_matrix:
                        flat_list += row.split(options.delimiter)
                    return flat_list

                options.args = flatten_concatenation(options.args)
    if not hasattr(options, 'dtype'):
        args = options.args
    else:
        dtype: object = locate(options.dtype[0])
        args = [dtype(arg) for arg in options.args]
        if options.reduce is not None:
            options.reduce = dtype(options.reduce)
    return args


def output(res: Any, out: TextIO):
    if out == sys.stdout:
        print(res)
    else:
        with open(out.name, 'w') as file:
            file.write(f"{res}")


if __name__ == '__main__':
    __program__ = sys.argv[0]
    parsed_cmd = parser.parse_args(sys.argv[1:])
    exit(main(options=parsed_cmd))
