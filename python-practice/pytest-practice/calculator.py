def add(a, b):
  return a + b

def divide(a, b):
  if b:
    return a / b
  raise ValueError("Cannot divide by zero")

def is_even(n):
  return n % 2 == 0

def multiply(a, b):
  return a * b
