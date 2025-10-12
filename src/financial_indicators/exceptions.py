class FinancialIndicatorError(Exception):
    """Base exception for all financial indicator errors."""

    pass


class InvalidInputError(FinancialIndicatorError):
    """Raised when input validation fails."""

    pass


class CalculationError(FinancialIndicatorError):
    """Raised when calculation cannot be completed."""

    pass


class ConvergenceError(FinancialIndicatorError):
    """Raised when iterative calculation fails to converge."""

    pass
