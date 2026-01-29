"""Example test file with intentional failures for FixBot demonstration."""

def add(a, b):
    """Simple addition function."""
    return a + b


def multiply(a, b):
    """Simple multiplication function."""
    return a * b


def test_addition():
    """Test addition - this will fail initially."""
    result = add(2, 3)
    assert result == 6  # Wrong! Should be 5


def test_multiplication():
    """Test multiplication - this should pass."""
    result = multiply(3, 4)
    assert result == 12


def test_another_addition():
    """Another addition test - this will also fail."""
    result = add(10, 20)
    assert result == 25  # Wrong! Should be 30
