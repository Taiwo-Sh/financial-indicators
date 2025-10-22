"""
Financial Indicators Package.

Python package for calculating essential financial and economic metrics.
"""

__version__ = "0.1.0"

import typing
from decimal import Decimal

from .core import *  # noqa


def d(value: typing.Union[str, float, int]) -> Decimal:
    """
    Convert a value to Decimal.

    :param value: The value to convert (str, float, or int).
    :return: The value as a Decimal.
    """
    return Decimal(str(value))
