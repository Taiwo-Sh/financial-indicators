"""Growth metrics for financial analysis."""

from decimal import Decimal

from feconomics.validation import validate_non_zero, validate_positive


def revenue_growth_rate(revenue_current: Decimal, revenue_previous: Decimal) -> Decimal:
    """
    Calculate Revenue Growth Rate.

    This metric measures the percentage change in revenue between periods,
    indicating business expansion or contraction.

    Formula:
        Revenue Growth Rate = [(Revenue_current - Revenue_previous) / Revenue_previous] x 100

    :param revenue_current: Revenue in the current period.
    :param revenue_previous: Revenue in the previous period. Must be non-zero.
    :return: Revenue growth rate as a percentage.
    :raises InvalidInputError: If revenue_previous is zero.

    Example:
        ```python
        from decimal import Decimal
        current = Decimal("1200000")
        previous = Decimal("1000000")
        growth = revenue_growth_rate(current, previous)
        print(growth)  # Decimal('20.00')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    validate_non_zero(revenue_previous, "revenue_previous")

    growth = ((revenue_current - revenue_previous) / revenue_previous) * 100
    return growth


def earnings_growth_rate(earnings_current: Decimal, earnings_previous: Decimal) -> Decimal:
    """
    Calculate Earnings Growth Rate.

    This metric measures the percentage change in earnings between periods,
    indicating profitability growth.

    Formula:
        Earnings Growth Rate = [(Earnings_current - Earnings_previous) / Earnings_previous] x 100

    :param earnings_current: Earnings in the current period.
    :param earnings_previous: Earnings in the previous period. Must be non-zero.
    :return: Earnings growth rate as a percentage.
    :raises InvalidInputError: If earnings_previous is zero.

    Example:
        ```python
        from decimal import Decimal
        current = Decimal("150000")
        previous = Decimal("120000")
        growth = earnings_growth_rate(current, previous)
        print(growth)  # Decimal('25.00')
        ```

    References:
        - Brigham, E., & Ehrhardt, M. (2020). Financial Management.
    """
    validate_non_zero(earnings_previous, "earnings_previous")

    growth = ((earnings_current - earnings_previous) / earnings_previous) * 100
    return growth


def compound_annual_growth_rate(
    ending_value: Decimal, beginning_value: Decimal, num_years: int
) -> Decimal:
    """
    Calculate Compound Annual Growth Rate (CAGR).

    CAGR represents the mean annual growth rate of an investment over
    a specified time period longer than one year.

    Formula:
        CAGR = [(Ending Value / Beginning Value)^(1/n) - 1] x 100
        Where n = Number of years

    :param ending_value: Final value.
    :param beginning_value: Initial value. Must be positive.
    :param num_years: Number of years. Must be positive.
    :return: CAGR as a percentage.
    :raises InvalidInputError: If beginning_value is not positive or num_years is not positive.

    Example:
        ```python
        from decimal import Decimal
        ending = Decimal("1500000")
        beginning = Decimal("1000000")
        years = 3
        cagr = compound_annual_growth_rate(ending, beginning, years)
        print(cagr)  # Decimal('14.47')
        ```

    References:
        - CFA Institute. (2021). Corporate Finance and Portfolio Management.
    """
    validate_positive(beginning_value, "beginning_value")
    if num_years <= 0:
        from feconomics.exceptions import InvalidInputError

        raise InvalidInputError(f"num_years must be positive, got {num_years}")

    # Calculate CAGR using fractional exponentiation
    ratio = ending_value / beginning_value
    exponent = 1 / Decimal(num_years)

    # Convert to float for power operation, then back to Decimal
    cagr = (Decimal(str(float(ratio) ** float(exponent))) - 1) * 100
    return cagr


def sustainable_growth_rate(roe: Decimal, dividend_payout_ratio: Decimal) -> Decimal:
    """
    Calculate Sustainable Growth Rate.

    Sustainable growth rate is the maximum rate at which a company can
    grow without requiring external financing, based on its profitability
    and dividend policy.

    Formula:
        Sustainable Growth Rate = ROE x (1 - Dividend Payout Ratio)

    :param roe: Return on Equity as a decimal (e.g., 0.20 for 20%).
    :param dividend_payout_ratio: Dividends / Net Income as a decimal.
    :return: Sustainable growth rate as a percentage.

    Example:
        ```python
        from decimal import Decimal
        roe = Decimal("0.15")  # 15%
        payout = Decimal("0.40")  # 40%
        sgr = sustainable_growth_rate(roe, payout)
        print(sgr)  # Decimal('9.00')
        ```

    References:
        - Ross, S., Westerfield, R., & Jordan, B. (2019). Fundamentals of Corporate Finance.
    """
    sgr = roe * (1 - dividend_payout_ratio) * 100
    return sgr


def retention_ratio(dividends: Decimal, net_income: Decimal) -> Decimal:
    """
    Calculate Retention Ratio (Plowback Ratio).

    The retention ratio is the proportion of earnings retained in the business
    rather than paid out as dividends.

    Formula:
        Retention Ratio = 1 - (Dividends / Net Income)

    :param dividends: Total dividends paid.
    :param net_income: Net income. Must be non-zero.
    :return: Retention ratio as a decimal.
    :raises InvalidInputError: If net_income is zero.

    Example:
        ```python
        from decimal import Decimal
        dividends = Decimal("40000")
        net_income = Decimal("100000")
        rr = retention_ratio(dividends, net_income)
        print(rr)  # Decimal('0.6000')
        ```

    References:
        - Bodie, Z., Kane, A., & Marcus, A. (2018). Investments.
    """
    validate_non_zero(net_income, "net_income")

    ratio = 1 - (dividends / net_income)
    return ratio
