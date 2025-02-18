from pathlib import Path  # pylint: disable=unused-import
from os.path import expanduser  # pylint: disable=unused-import

import pytest

import numpy as np
from .context import check_and_display, load_tokenization_raw, load_tokenization_tokenized, CORPUS_SIZE, \
    tok_eval


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data")).exists()')
def test_raw():
    raw = load_tokenization_raw()

    assert sum(1 for _ in raw) == CORPUS_SIZE


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data")).exists()')
def test_tokenized():
    tokenized = load_tokenization_tokenized()

    assert sum(1 for _ in tokenized) == CORPUS_SIZE


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data")).exists()')
def test_metadata():
    stats = check_and_display("~/.sadedegel_data")

    assert stats['byte']['raw'] * 1e6 >= 1 * 1024 * 1024
    assert stats['byte']['raw'] * 1e6 >= 1 * 1024 * 1024


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data")).exists()')
def test_evaluator():
    table = tok_eval(["simple", "bert"], limit=1000)

    assert float(table[0][1]) > 0.83
    assert float(table[0][2]) > 0.83
    assert float(table[1][1]) > 0.86
    assert float(table[1][2]) > 0.86
