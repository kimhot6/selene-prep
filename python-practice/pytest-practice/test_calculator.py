import pytest
from calculator import add, divide, is_even, multiply

def test_add_positive():
  assert add(2, 3) == 5
  
def test_add_negative():
  assert add(-1,-2) == -3

def test_divide_normal():
  assert divide(6, 3) == 2
  
def test_divide_zero():
  # 예외 발생 테스트
  with pytest.raises(ValueError):
    divide(10, 0)
    
def test_is_even():
  assert is_even(3) is False
  assert is_even(4) is True
  
@pytest.mark.parametrize("n,expected", [
  (0, True),
  (1, False),
  (-2, True),
  (100, True),
])
def test_is_even_many(n, expected):
  assert is_even(n) == expected
  
def test_multiply():
  assert multiply(3, 5) == 15
    
@pytest.mark.parametrize("a,b,expected", [
  (3,4,12),
  (0,8,0),
  (2,-9,-18),
])
def test_multiply_many(a, b, expected):
  assert multiply(a, b) == expected
