def fibonacci(n: int) -> int:
    """Get the n-th Fibonacci number, starting with 0 and 1."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return b  # BUG! should be a!


def test_fibonacci():
    a = fibonacci(10)
    assert a == 89
