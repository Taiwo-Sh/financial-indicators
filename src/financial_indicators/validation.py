"""Input validation utilities for financial indicators."""

from decimal import Decimal
from typing import Any, Sequence

from financial_indicators.exceptions import InvalidInputError


def validate_positive(value: Decimal, param_name: str) -> None:
    """
    Validate that a value is positive.

    :param value: The value to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If value is not positive.
    """
    if value <= 0:
        raise InvalidInputError(f"{param_name} must be positive, got {value}")


def validate_non_negative(value: Decimal, param_name: str) -> None:
    """
    Validate that a value is non-negative.

    :param value: The value to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If value is negative.
    """
    if value < 0:
        raise InvalidInputError(f"{param_name} must be non-negative, got {value}")


def validate_non_empty(sequence: Sequence[Any], param_name: str) -> None:
    """
    Validate that a sequence is not empty.

    :param sequence: The sequence to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If sequence is empty.
    """
    if not sequence:
        raise InvalidInputError(f"{param_name} cannot be empty")


def validate_percentage(value: Decimal, param_name: str) -> None:
    """
    Validate that a value represents a valid percentage (0-100).

    :param value: The value to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If value is not between 0 and 100.
    """
    if not (0 <= value <= 100):
        raise InvalidInputError(f"{param_name} must be between 0 and 100, got {value}")


def validate_rate(value: Decimal, param_name: str) -> None:
    """
    Validate that a value represents a valid rate (0-1).

    :param value: The value to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If value is not between 0 and 1.
    """
    if not (0 <= value <= 1):
        raise InvalidInputError(f"{param_name} must be between 0 and 1, got {value}")


def validate_non_zero(value: Decimal, param_name: str) -> None:
    """
    Validate that a value is not zero.

    :param value: The value to validate.
    :param param_name: The name of the parameter being validated.
    :raises InvalidInputError: If value is zero.
    """
    if value == 0:
        raise InvalidInputError(f"{param_name} cannot be zero")
