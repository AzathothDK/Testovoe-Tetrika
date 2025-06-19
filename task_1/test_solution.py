import pytest
from solution import strict

@strict
def add(a: int, b: int) -> int:
    return a + b

@strict
def join_strings(a: str, b: str) -> str:
    return a + b

def test_add_valid():
    assert add(1, 2) == 3

def test_add_invalid_type():
    with pytest.raises(TypeError):
        add(1, "2")

def test_join_valid():
    assert join_strings("a", "b") == "ab"

def test_join_invalid():
    with pytest.raises(TypeError):
        join_strings("a", 2)
