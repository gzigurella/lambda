import pytest
from shlex import split as shellsplit

from src.constants import VERSION
from src.main import main as entrypoint, version


def test_positional_arguments():
    exit_code, msg = entrypoint(shellsplit('lambda -D --dtype=int "#1+#2" 2 4 5'))
    assert exit_code == 0 and msg is None


def test_list_arguments():
    exit_code, msg = entrypoint(shellsplit('lambda -D --dtype=int "#i+1 for #i in #?" 2 4 5 10'))
    assert exit_code == 0 and msg is None


def test_list_file():
    exit_code, msg = entrypoint(shellsplit('lambda -D --dtype=int "#i+42 for #i in #?" -f in.txt -d ","'))
    assert exit_code == 0 and msg is None


def test_reduce_and_output():
    exit_code, msg = entrypoint(shellsplit('lambda --reduce 0 -D --dtype=int "#1+#2" 2 4 20 24 -o out.txt'))
    assert exit_code == 0 and msg is None


def test_lambda_script():
    import os
    script = os.path.abspath("./text.lambda")
    exit_code, msg = entrypoint(shellsplit(f'lambda -D --dtype=int script::{script} 2 4'))
    assert exit_code == 0 and msg is None

def test_import_module():
    exit_code, msg = entrypoint(shellsplit(f'-D --dtype=int --module=numpy "#i+numpy.random.default_rng().random() for #i in #?" 1 2 3 4 5 6 7 9 0'))
    assert exit_code == 0 and msg is None
