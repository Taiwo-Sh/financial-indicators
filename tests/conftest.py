"""Shared test configuration and fixtures."""

from decimal import ROUND_HALF_UP, Decimal


def quantize_decimal(value: Decimal, decimal_places: int = 2) -> Decimal:
    """
    Quantize a Decimal value to a specific number of decimal places.
    
    Args:
        value: The Decimal value to quantize
        decimal_places: Number of decimal places (default: 2)
        
    Returns:
        Quantized Decimal value
        
    Example:
        >>> quantize_decimal(Decimal("12.3456"), 2)
        Decimal('12.35')
    """
    quantizer = Decimal(10) ** -decimal_places
    return value.quantize(quantizer, rounding=ROUND_HALF_UP)


def assert_decimal_equal(actual: Decimal, expected: Decimal, decimal_places: int = 2):
    """
    Assert that two Decimal values are equal after quantization.
    
    Args:
        actual: Actual value from function
        expected: Expected value
        decimal_places: Number of decimal places to compare (default: 2)
        
    Raises:
        AssertionError: If values don't match after quantization
    """
    actual_quantized = quantize_decimal(actual, decimal_places)
    expected_quantized = quantize_decimal(expected, decimal_places)
    assert actual_quantized == expected_quantized, (
        f"Expected {expected_quantized}, but got {actual_quantized}"
    )
