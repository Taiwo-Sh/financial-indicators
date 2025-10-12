"""Risk metrics for financial analysis."""

import typing
from decimal import Decimal

from financial_indicators.exceptions import InvalidInputError
from financial_indicators.validation import validate_non_empty, validate_positive


def beta(
    asset_returns: typing.Sequence[Decimal], market_returns: typing.Sequence[Decimal]
) -> Decimal:
    """
    Calculate Beta (Systematic Risk).

    Beta measures an asset's volatility relative to the overall market.
    It indicates how much the asset's return is expected to change
    given a change in market returns.

    Formula:
        β = Covariance(R_asset, R_market) / Variance(R_market)

    Interpretation:
        - β > 1.0: More volatile than market
        - β = 1.0: Moves with market
        - β < 1.0: Less volatile than market
        - β < 0.0: Moves opposite to market

    :param asset_returns: typing.Sequence of asset returns.
    :param market_returns: typing.Sequence of market returns. Must be same length as asset_returns.
    :return: Beta coefficient.
    :raises InvalidInputError: If typing.Sequences are empty or have different lengths.

    Example:
        ```python
        from decimal import Decimal
        asset = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        market = [Decimal("0.08"), Decimal("0.04"), Decimal("-0.01"), Decimal("0.06")]
        b = beta(asset, market)
        print(b)  # Approximately 1.2
        ```

    References:
        - Sharpe, W. (1964). Capital Asset Prices.
    """
    validate_non_empty(asset_returns, "asset_returns")
    validate_non_empty(market_returns, "market_returns")

    if len(asset_returns) != len(market_returns):
        raise InvalidInputError(
            f"asset_returns and market_returns must have same length, "
            f"got {len(asset_returns)} and {len(market_returns)}"
        )

    n = Decimal(len(asset_returns))

    # Calculate means
    asset_mean = sum(asset_returns) / n
    market_mean = sum(market_returns) / n

    # Calculate covariance and variance
    covariance = sum(
        (a - asset_mean) * (m - market_mean)
        for a, m in zip(asset_returns, market_returns, strict=True)
    ) / (n - 1)

    market_variance = sum((m - market_mean) ** 2 for m in market_returns) / (
        n - 1
    )

    if market_variance == 0:
        raise InvalidInputError("market_returns has zero variance")

    beta_val = covariance / market_variance
    return beta_val


def standard_deviation(returns: typing.Sequence[Decimal]) -> Decimal:
    """
    Calculate Standard Deviation of returns.

    Standard deviation measures the dispersion of returns around the mean,
    indicating volatility or risk.

    Formula:
        σ = √[Σ(xᵢ - μ)² / (n-1)]

    :param returns: typing.Sequence of return values.
    :return: Standard deviation.
    :raises InvalidInputError: If returns is empty or has only one element.

    Example:
        ```python
        from decimal import Decimal
        returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        sd = standard_deviation(returns)
        print(sd)  # Decimal('0.0519')
        ```

    References:
        - Bodie, Z., Kane, A., & Marcus, A. (2018). Investments.
    """
    validate_non_empty(returns, "returns")

    if len(returns) < 2:
        raise InvalidInputError("returns must have at least 2 elements for standard deviation")

    n = Decimal(len(returns))
    mean = sum(returns) / n

    variance = sum((r - mean) ** 2 for r in returns) / (n - 1)

    # Calculate square root using Decimal's sqrt
    std_dev = variance.sqrt()
    return std_dev


def variance(returns: typing.Sequence[Decimal]) -> Decimal:
    """
    Calculate Variance of returns.

    Variance measures the spread of returns around the mean, representing risk.

    Formula:
        Variance = Σ(xᵢ - μ)² / (n-1)

    :param returns: typing.Sequence of return values.
    :return: Variance.
    :raises InvalidInputError: If returns is empty or has only one element.

    Example:
        ```python
        from decimal import Decimal
        returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        var = variance(returns)
        print(var)  # Decimal('0.0027')
        ```

    References:
        - CFA Institute. (2021). Quantitative Methods.
    """
    validate_non_empty(returns, "returns")

    if len(returns) < 2:
        raise InvalidInputError("returns must have at least 2 elements for variance")

    n = Decimal(len(returns))
    mean = sum(returns) / n

    var = sum((r - mean) ** 2 for r in returns) / (n - 1)
    return var


def sharpe_ratio(
    portfolio_return: Decimal, risk_free_rate: Decimal, portfolio_std_dev: Decimal
) -> Decimal:
    """
    Calculate Sharpe Ratio.

    The Sharpe ratio measures risk-adjusted return by comparing excess
    return to standard deviation.

    Formula:
        Sharpe Ratio = (R_portfolio - R_risk_free) / σ_portfolio

    :param portfolio_return: Expected or actual portfolio return as decimal.
    :param risk_free_rate: Risk-free rate as decimal.
    :param portfolio_std_dev: Portfolio standard deviation. Must be positive.
    :return: Sharpe ratio.
    :raises InvalidInputError: If portfolio_std_dev is not positive.

    Example:
        ```python
        from decimal import Decimal
        ret = Decimal("0.12")
        rf = Decimal("0.02")
        std = Decimal("0.15")
        sr = sharpe_ratio(ret, rf, std)
        print(sr)  # Decimal('0.6667')
        ```

    References:
        - Sharpe, W. (1966). Mutual Fund Performance.
    """
    validate_positive(portfolio_std_dev, "portfolio_std_dev")

    ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return ratio


def sortino_ratio(
    portfolio_return: Decimal, risk_free_rate: Decimal, downside_deviation: Decimal
) -> Decimal:
    """
    Calculate Sortino Ratio.

    The Sortino ratio is similar to the Sharpe ratio but only considers
    downside volatility, penalizing only negative returns.

    Formula:
        Sortino Ratio = (R_portfolio - R_risk_free) / σ_downside

    :param portfolio_return: Expected or actual portfolio return as decimal.
    :param risk_free_rate: Risk-free rate as decimal.
    :param downside_deviation: Standard deviation of negative returns only. Must be positive.
    :return: Sortino ratio.
    :raises InvalidInputError: If downside_deviation is not positive.

    Example:
        ```python
        from decimal import Decimal
        ret = Decimal("0.12")
        rf = Decimal("0.02")
        dd = Decimal("0.10")
        sr = sortino_ratio(ret, rf, dd)
        print(sr)  # Decimal('1.0000')
        ```

    References:
        - Sortino, F., & Price, L. (1994). Performance Measurement.
    """
    validate_positive(downside_deviation, "downside_deviation")

    ratio = (portfolio_return - risk_free_rate) / downside_deviation
    return ratio


def value_at_risk_historical(
    returns: typing.Sequence[Decimal], portfolio_value: Decimal, confidence_level: Decimal
) -> Decimal:
    """
    Calculate Value at Risk (VaR) using Historical Method.

    VaR estimates the maximum loss over a specified time period at
    a given confidence level.

    Formula:
        VaR = Portfolio Value x percentile(returns, (1 - confidence_level))

    :param returns: Historical returns as decimals.
    :param portfolio_value: Current portfolio value.
    :param confidence_level: Confidence level as decimal (e.g., 0.95 for 95%).
    :return: VaR as a positive loss amount.
    :raises InvalidInputError: If returns is empty.

    Example:
        ```python
        from decimal import Decimal
        returns = [Decimal("-0.05"), Decimal("0.02"), Decimal("0.03"), Decimal("-0.01")]
        value = Decimal("1000000")
        confidence = Decimal("0.95")
        var = value_at_risk_historical(returns, value, confidence)
        print(var)  # Maximum expected loss at 95% confidence
        ```

    References:
        - Jorion, P. (2006). Value at Risk.
    """
    validate_non_empty(returns, "returns")

    # Sort returns
    sorted_returns = sorted(returns)

    # Find the percentile
    percentile_index = int((1 - confidence_level) * Decimal(len(sorted_returns)))
    percentile_return = sorted_returns[max(0, percentile_index)]

    # VaR is the loss (negative return x portfolio value)
    var = abs(percentile_return * portfolio_value)
    return var


def conditional_var(
    returns: typing.Sequence[Decimal], portfolio_value: Decimal, confidence_level: Decimal
) -> Decimal:
    """
    Calculate Conditional VaR (CVaR) / Expected Shortfall.

    CVaR measures the expected loss given that the loss exceeds VaR.
    It provides a more comprehensive risk measure than VaR.

    Formula:
        CVaR = Average of returns below VaR threshold

    :param returns: Historical returns as decimals.
    :param portfolio_value: Current portfolio value.
    :param confidence_level: Confidence level as decimal (e.g., 0.95 for 95%).
    :return: CVaR as a positive expected loss amount.
    :raises InvalidInputError: If returns is empty.

    Example:
        ```python
        from decimal import Decimal
        returns = [Decimal("-0.05"), Decimal("0.02"), Decimal("-0.03"), Decimal("-0.01")]
        value = Decimal("1000000")
        confidence = Decimal("0.95")
        cvar = conditional_var(returns, value, confidence)
        print(cvar)  # Expected loss beyond VaR
        ```

    References:
        - Rockafellar, R.T., & Uryasev, S. (2000). Optimization of CVaR.
    """
    validate_non_empty(returns, "returns")

    # Sort returns
    sorted_returns = sorted(returns)

    # Find the cutoff
    cutoff_index = int((1 - confidence_level) * Decimal(len(sorted_returns)))

    # Average of worst returns
    tail_returns = sorted_returns[: max(1, cutoff_index + 1)]
    avg_tail_return = sum(tail_returns) / Decimal(len(tail_returns))

    # CVaR is the expected loss
    cvar = abs(avg_tail_return * portfolio_value)
    return cvar


def maximum_drawdown(values: typing.Sequence[Decimal]) -> Decimal:
    """
    Calculate Maximum Drawdown.

    Maximum drawdown measures the largest peak-to-trough decline in
    portfolio value, indicating worst-case loss.

    Formula:
        Maximum Drawdown = (Trough Value - Peak Value) / Peak Value

    :param values: Time series of portfolio values.
    :return: Maximum drawdown as a positive percentage.
    :raises InvalidInputError: If values is empty.

    Example:
        ```python
        from decimal import Decimal
        values = [100, Decimal("110"), Decimal("105"), Decimal("95"), 100]
        mdd = maximum_drawdown(values)
        print(mdd)  # Decimal('13.64')
        ```

    References:
        - Magdon-Ismail, M., & Atiya, A. (2004). Maximum Drawdown.
    """
    validate_non_empty(values, "values")

    max_dd = 0
    peak = values[0]

    for value in values[1:]:
        if value > peak:
            peak = value
        else:
            drawdown = (peak - value) / peak
            if drawdown > max_dd:
                max_dd = drawdown

    return Decimal(max_dd * 100)
