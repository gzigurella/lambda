import pytest
from shlex import split as shellsplit

from src.constants import VERSION
from src.main import main as entrypoint, version


def test_positional_arguments():
    assert entrypoint(shellsplit('lambda -D --dtype=int "$1+$2" 2 4 5')) == 0


def test_list_arguments():
    assert entrypoint(shellsplit('lambda -D --dtype=int "$i+1 for $i in $@" 2 4 5 10')) == 0


def test_list_file():
    assert entrypoint(shellsplit('lambda -D --dtype=int "$i+42 for $i in $@" -f in.txt -d ","')) == 0


def test_reduce_and_output():
    assert entrypoint(shellsplit('lambda --reduce 0 -D --dtype=int "$1+$2" 2 4 20 24 -o out.txt')) == 0


def test_lambda_script():
    import os
    script = os.path.abspath("./text.lambda")
    assert entrypoint(shellsplit(f'lambda -D --dtype=int script::{script} 2 4')) == 0
