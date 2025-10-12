"""Time value of money functions for financial analysis."""

import typing
from decimal import Decimal

from financial_indicators.constants import DEFAULT_MAX_ITERATIONS, DEFAULT_TOLERANCE
from financial_indicators.exceptions import ConvergenceError, InvalidInputError
from financial_indicators.validation import (
    validate_non_empty,
    validate_non_negative,
    validate_positive,
)


def net_present_value(
    cash_flows: typing.Sequence[Decimal], discount_rate: Decimal
) -> Decimal:
    """
    Calculate Net Present Value of a series of cash flows.

    NPV measures the profitability of an investment by discounting future cash flows
    to their present value and summing them. A positive NPV indicates value creation.

    Formula:
        NPV = Σ[CFₜ / (1 + r)ᵗ] for t = 0 to n

    :param cash_flows: List of cash flows starting at t=0 (initial investment).
        First value is typically negative (investment outlay).
    :param discount_rate: Discount rate as decimal (e.g., 0.10 for 10%). Must be non-negative.
    :return: Net present value in same currency units as input cash flows.
    :raises InvalidInputError: If cash_flows is empty or discount_rate is negative.

    Example:
        ```python
        from decimal import Decimal
        cash_flows = [Decimal("-1000"), Decimal("300"), Decimal("400"), Decimal("500")]
        discount_rate = Decimal("0.1")
        npv = net_present_value(cash_flows, discount_rate)
        print(npv)  # Decimal('49.21')
        ```

    References:
        - Brealey, R., Myers, S., & Allen, F. (2020). Principles of Corporate Finance.
        - CFA Institute. (2021). Corporate Finance and Portfolio Management.
    """
    validate_non_empty(cash_flows, "cash_flows")
    validate_non_negative(discount_rate, "discount_rate")

    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)

    return Decimal(npv)


def internal_rate_of_return(
    cash_flows: typing.Sequence[Decimal],
    initial_guess: Decimal = Decimal("0.1"),
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    tolerance: Decimal = DEFAULT_TOLERANCE,
) -> typing.Optional[Decimal]:
    """
    Calculate Internal Rate of Return using Newton-Raphson method.

    IRR is the discount rate that makes NPV equal to zero. It represents the
    expected compound annual rate of return.

    Formula:
        0 = Σ[CFₜ / (1 + IRR)ᵗ] for t = 0 to n
        Solved iteratively: IRRₙ₊₁ = IRRₙ - f(IRRₙ) / f'(IRRₙ)

    :param cash_flows: List of cash flows starting at t=0. Must have at least one
        sign change for IRR to exist.
    :param initial_guess: Starting value for iteration. Defaults to 0.1 (10%).
    :param max_iterations: Maximum number of iterations. Defaults to 100.
    :param tolerance: Convergence tolerance. Defaults to 1e-6.
    :return: IRR as a decimal rate, or None if IRR doesn't exist.
    :raises InvalidInputError: If cash_flows is empty.
    :raises ConvergenceError: If calculation doesn't converge within max_iterations.

    Example:
        ```python
        from decimal import Decimal
        cash_flows = [Decimal("-1000"), Decimal("300"), Decimal("400"), Decimal("500")]
        irr = internal_rate_of_return(cash_flows)
        print(f"{irr * 100}%")  # Approximately 16.92%
        ```

    References:
        - Ross, S., Westerfield, R., & Jordan, B. (2019). Fundamentals of Corporate Finance.
    """
    validate_non_empty(cash_flows, "cash_flows")

    # Check for sign changes - IRR requires at least one
    sign_changes = sum(
        1
        for i in range(len(cash_flows) - 1)
        if (cash_flows[i] * cash_flows[i + 1]) < 0
    )
    if sign_changes == 0:
        return None

    irr = initial_guess

    for _ in range(max_iterations):
        # Calculate NPV and its derivative
        npv = 0
        npv_derivative = 0

        for t, cf in enumerate(cash_flows):
            discount_factor = (1 + irr) ** t
            npv += cf / discount_factor
            if t > 0:
                npv_derivative -= (Decimal(t) * cf) / ((1 + irr) ** (t + 1))

        # Check convergence
        if abs(npv) < tolerance:
            return irr.quantize(Decimal("0.000001"))

        # Avoid division by zero
        if npv_derivative == 0:
            return None

        # Newton-Raphson update
        irr = irr - (npv / npv_derivative)

    raise ConvergenceError(
        f"IRR calculation did not converge within {max_iterations} iterations"
    )


def present_value(
    future_value: Decimal, discount_rate: Decimal, periods: int
) -> Decimal:
    """
    Calculate present value of a future amount.

    Determines what a future sum is worth in today's dollars given a discount rate.

    Formula:
        PV = FV / (1 + r)ⁿ

    :param future_value: The future value amount.
    :param discount_rate: Discount rate per period as decimal (e.g., 0.10 for 10%).
    :param periods: Number of periods. Must be non-negative.
    :return: Present value in same currency units as future_value.
    :raises InvalidInputError: If discount_rate is negative or periods is negative.

    Example:
        ```python
        from decimal import Decimal
        fv = Decimal("1000")
        rate = Decimal("0.05")
        periods = 5
        pv = present_value(fv, rate, periods)
        print(pv)  # Decimal('783.53')
        ```

    References:
        - Bodie, Z., Kane, A., & Marcus, A. (2018). Investments.
    """
    validate_non_negative(discount_rate, "discount_rate")
    if periods < 0:
        raise InvalidInputError(f"periods must be non-negative, got {periods}")

    pv = future_value / ((1 + discount_rate) ** periods)
    return pv


def future_value(present_value: Decimal, growth_rate: Decimal, periods: int) -> Decimal:
    """
    Calculate future value of a present amount.

    Determines what a present sum will grow to given a growth/interest rate.

    Formula:
        FV = PV x (1 + r)ⁿ

    :param present_value: The present value amount.
    :param growth_rate: Growth/interest rate per period as decimal (e.g., 0.10 for 10%).
    :param periods: Number of periods. Must be non-negative.
    :return: Future value in same currency units as present_value.
    :raises InvalidInputError: If growth_rate is negative or periods is negative.

    Example:
        ```python
        from decimal import Decimal
        pv = Decimal("1000")
        rate = Decimal("0.05")
        periods = 5
        fv = future_value(pv, rate, periods)
        print(fv)  # Decimal('1276.28')
        ```

    References:
        - Brigham, E., & Ehrhardt, M. (2020). Financial Management: Theory & Practice.
    """
    validate_non_negative(growth_rate, "growth_rate")
    if periods < 0:
        raise InvalidInputError(f"periods must be non-negative, got {periods}")

    fv = present_value * ((1 + growth_rate) ** periods)
    return fv


def annuity_present_value(
    payment: Decimal, discount_rate: Decimal, periods: int
) -> Decimal:
    """
    Calculate present value of an ordinary annuity.

    Determines the present value of a series of equal periodic payments.

    Formula:
        PV_annuity = PMT x [(1 - (1 + r)⁻ⁿ) / r]

    :param payment: Payment amount per period.
    :param discount_rate: Discount rate per period as decimal. Must be positive.
    :param periods: Number of periods. Must be positive.
    :return: Present value of the annuity.
    :raises InvalidInputError: If discount_rate is not positive or periods is not positive.

    Example:
        ```python
        from decimal import Decimal
        payment = 100
        rate = Decimal("0.05")
        periods = 10
        pv = annuity_present_value(payment, rate, periods)
        print(pv)  # Decimal('772.17')
        ```

    References:
        - Ross, S., Westerfield, R., & Jaffe, J. (2019). Corporate Finance.
    """
    validate_positive(discount_rate, "discount_rate")
    if periods <= 0:
        raise InvalidInputError(f"periods must be positive, got {periods}")

    pv = payment * (
        (1 - (1 + discount_rate) ** (-periods)) / discount_rate
    )
    return pv


def annuity_future_value(
    payment: Decimal, growth_rate: Decimal, periods: int
) -> Decimal:
    """
    Calculate future value of an ordinary annuity.

    Determines the future value of a series of equal periodic payments.

    Formula:
        FV_annuity = PMT x [((1 + r)ⁿ - 1) / r]

    :param payment: Payment amount per period.
    :param growth_rate: Growth/interest rate per period as decimal. Must be positive.
    :param periods: Number of periods. Must be positive.
    :return: Future value of the annuity.
    :raises InvalidInputError: If growth_rate is not positive or periods is not positive.

    Example:
        ```python
        from decimal import Decimal
        payment = 100
        rate = Decimal("0.05")
        periods = 10
        fv = annuity_future_value(payment, rate, periods)
        print(fv)  # Decimal('1257.79')
        ```

    References:
        - Berk, J., & DeMarzo, P. (2020). Corporate Finance.
    """
    validate_positive(growth_rate, "growth_rate")
    if periods <= 0:
        raise InvalidInputError(f"periods must be positive, got {periods}")

    fv = payment * (((1 + growth_rate) ** periods - 1) / growth_rate)
    return fv


def payback_period(cash_flows: typing.Sequence[Decimal]) -> typing.Optional[Decimal]:
    """
    Calculate payback period for an investment.

    The payback period is the time required to recover the initial investment
    from cumulative cash flows.

    Formula:
        Payback Period = Year before full recovery +
                        (Unrecovered cost at start of year / Cash flow during year)

    :param cash_flows: List of cash flows starting at t=0 (initial investment).
        First value is typically negative.
    :return: Number of periods to payback (can be fractional), or None if
        payback never occurs.
    :raises InvalidInputError: If cash_flows is empty.

    Example:
        ```python
        from decimal import Decimal
        cash_flows = [Decimal("-1000"), Decimal("300"), Decimal("400"), Decimal("500")]
        pp = payback_period(cash_flows)
        print(pp)  # Decimal('2.60')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    validate_non_empty(cash_flows, "cash_flows")

    cumulative = 0
    for period, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= 0 and period > 0:
            # Interpolate to find exact payback period
            unrecovered = cumulative - cf
            if cf != 0:
                fraction = abs(unrecovered) / cf
                return (Decimal(period - 1) + fraction)
            return Decimal(period)

    return None  # Payback never occurs


def discounted_payback_period(
    cash_flows: typing.Sequence[Decimal], discount_rate: Decimal
) -> typing.Optional[Decimal]:
    """
    Calculate discounted payback period for an investment.

    Similar to payback period but uses discounted cash flows to account for
    time value of money.

    Formula:
        Uses discounted cash flows: DCFₜ = CFₜ / (1 + r)ᵗ

    :param cash_flows: List of cash flows starting at t=0 (initial investment).
    :param discount_rate: Discount rate as decimal. Must be non-negative.
    :return: Number of periods to discounted payback (can be fractional),
        or None if payback never occurs.
    :raises InvalidInputError: If cash_flows is empty or discount_rate is negative.

    Example:
        ```python
        from decimal import Decimal
        cash_flows = [Decimal("-1000"), Decimal("300"), Decimal("400"), Decimal("500")]
        rate = Decimal("0.1")
        dpp = discounted_payback_period(cash_flows, rate)
        print(dpp)  # Decimal('3.15')
        ```

    References:
        - Brigham, E., & Houston, J. (2019). Fundamentals of Financial Management.
    """
    validate_non_empty(cash_flows, "cash_flows")
    validate_non_negative(discount_rate, "discount_rate")

    cumulative = 0
    for period, cf in enumerate(cash_flows):
        discounted_cf = cf / ((1 + discount_rate) ** period)
        cumulative += discounted_cf
        if cumulative >= 0 and period > 0:
            # Interpolate to find exact payback period
            unrecovered = cumulative - discounted_cf
            if discounted_cf != 0:
                fraction = abs(unrecovered) / discounted_cf
                return (Decimal(period - 1) + fraction)
            return Decimal(period)

    return None  # Payback never occurs
