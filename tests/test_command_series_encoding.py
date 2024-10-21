import pytest

from solver import encode_commandseries
from solver import decode_commandseries

def test_empty():
    assert decode_commandseries(0) == []

def test_single():
    assert encode_commandseries([], 14) == 15
    assert decode_commandseries(15) == [14]

def test_full():
    expected = [14, 21, 1, 0, 0, 17, 20, 4, 0]
    encoded = encode_commandseries(expected[:-1], expected[-1])
    assert decode_commandseries(encoded) == expected