"""Tests for risk metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.risk import (
    beta,
    conditional_var,
    maximum_drawdown,
    sharpe_ratio,
    sortino_ratio,
    standard_deviation,
    value_at_risk_historical,
    variance,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestBeta:
    """Test suite for beta function."""

    def test_beta_standard(self):
        """Test beta calculation with standard inputs."""
        asset_returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        market_returns = [Decimal("0.08"), Decimal("0.04"), Decimal("-0.01"), Decimal("0.06")]
        result = beta(asset_returns=asset_returns, market_returns=market_returns)
        # Should be around 1.2 based on covariance/variance
        assert Decimal("1.0") < result < Decimal("1.5")

    def test_beta_high_volatility(self):
        """Test beta with high volatility asset."""
        asset_returns = [Decimal("0.15"), Decimal("-0.10"), Decimal("0.20"), Decimal("-0.05")]
        market_returns = [Decimal("0.05"), Decimal("-0.03"), Decimal("0.06"), Decimal("-0.01")]
        result = beta(asset_returns=asset_returns, market_returns=market_returns)
        assert result > Decimal("1.0")  # More volatile than market

    def test_beta_low_volatility(self):
        """Test beta with low volatility asset."""
        asset_returns = [Decimal("0.02"), Decimal("0.01"), Decimal("-0.01"), Decimal("0.02")]
        market_returns = [Decimal("0.05"), Decimal("0.03"), Decimal("-0.02"), Decimal("0.04")]
        result = beta(asset_returns=asset_returns, market_returns=market_returns)
        assert result < Decimal("1.0")  # Less volatile than market

    def test_beta_empty_returns_raises_error(self):
        """Test that empty returns raises error."""
        with pytest.raises(InvalidInputError):
            beta(asset_returns=[], market_returns=[])

    def test_beta_mismatched_lengths_raises_error(self):
        """Test that mismatched lengths raises error."""
        asset_returns = [Decimal("0.10"), Decimal("0.05")]
        market_returns = [Decimal("0.08"), Decimal("0.04"), Decimal("-0.01")]
        with pytest.raises(InvalidInputError):
            beta(asset_returns=asset_returns, market_returns=market_returns)

    def test_beta_zero_market_variance_raises_error(self):
        """Test that zero market variance raises error."""
        asset_returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02")]
        market_returns = [Decimal("0.08"), Decimal("0.08"), Decimal("0.08")]  # No variance
        with pytest.raises(InvalidInputError):
            beta(asset_returns=asset_returns, market_returns=market_returns)


class TestStandardDeviation:
    """Test suite for standard_deviation function."""

    def test_std_dev_standard(self):
        """Test standard deviation with standard inputs."""
        returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        result = standard_deviation(returns=returns)
        # Should be around 0.05
        assert Decimal("0.04") < result < Decimal("0.06")

    def test_std_dev_low_volatility(self):
        """Test standard deviation with low volatility."""
        returns = [Decimal("0.02"), Decimal("0.02"), Decimal("0.02"), Decimal("0.02")]
        result = standard_deviation(returns=returns)
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_std_dev_high_volatility(self):
        """Test standard deviation with high volatility."""
        returns = [Decimal("0.20"), Decimal("-0.15"), Decimal("0.18"), Decimal("-0.10")]
        result = standard_deviation(returns=returns)
        assert result > Decimal("0.15")  # High volatility

    def test_std_dev_empty_raises_error(self):
        """Test that empty returns raises error."""
        with pytest.raises(InvalidInputError):
            standard_deviation(returns=[])

    def test_std_dev_single_value_raises_error(self):
        """Test that single value raises error."""
        with pytest.raises(InvalidInputError):
            standard_deviation(returns=[Decimal("0.10")])


class TestVariance:
    """Test suite for variance function."""

    def test_variance_standard(self):
        """Test variance with standard inputs."""
        returns = [Decimal("0.10"), Decimal("0.05"), Decimal("-0.02"), Decimal("0.08")]
        result = variance(returns=returns)
        # Should be around 0.0027
        assert Decimal("0.002") < result < Decimal("0.004")

    def test_variance_no_variability(self):
        """Test variance with no variability."""
        returns = [Decimal("0.05"), Decimal("0.05"), Decimal("0.05"), Decimal("0.05")]
        result = variance(returns=returns)
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_variance_empty_raises_error(self):
        """Test that empty returns raises error."""
        with pytest.raises(InvalidInputError):
            variance(returns=[])

    def test_variance_single_value_raises_error(self):
        """Test that single value raises error."""
        with pytest.raises(InvalidInputError):
            variance(returns=[Decimal("0.10")])


class TestSharpeRatio:
    """Test suite for sharpe_ratio function."""

    def test_sharpe_ratio_positive(self):
        """Test Sharpe ratio with positive excess return."""
        portfolio_return = Decimal("0.12")
        risk_free_rate = Decimal("0.02")
        portfolio_std_dev = Decimal("0.15")
        result = sharpe_ratio(
            portfolio_return=portfolio_return,
            risk_free_rate=risk_free_rate,
            portfolio_std_dev=portfolio_std_dev,
        )
        assert_decimal_equal(actual=result, expected=Decimal("0.6667"))

    def test_sharpe_ratio_high(self):
        """Test Sharpe ratio with high risk-adjusted return."""
        portfolio_return = Decimal("0.20")
        risk_free_rate = Decimal("0.02")
        portfolio_std_dev = Decimal("0.10")
        result = sharpe_ratio(
            portfolio_return=portfolio_return,
            risk_free_rate=risk_free_rate,
            portfolio_std_dev=portfolio_std_dev,
        )
        assert_decimal_equal(actual=result, expected=Decimal("1.8000"))

    def test_sharpe_ratio_negative(self):
        """Test Sharpe ratio with underperformance."""
        portfolio_return = Decimal("0.01")
        risk_free_rate = Decimal("0.02")
        portfolio_std_dev = Decimal("0.10")
        result = sharpe_ratio(
            portfolio_return=portfolio_return,
            risk_free_rate=risk_free_rate,
            portfolio_std_dev=portfolio_std_dev,
        )
        assert result < 0  # Negative Sharpe ratio

    def test_sharpe_ratio_zero_std_dev_raises_error(self):
        """Test that zero standard deviation raises error."""
        with pytest.raises(InvalidInputError):
            sharpe_ratio(
                portfolio_return=Decimal("0.12"),
                risk_free_rate=Decimal("0.02"),
                portfolio_std_dev=Decimal("0"),
            )


class TestSortinoRatio:
    """Test suite for sortino_ratio function."""

    def test_sortino_ratio_positive(self):
        """Test Sortino ratio with positive excess return."""
        portfolio_return = Decimal("0.12")
        risk_free_rate = Decimal("0.02")
        downside_deviation = Decimal("0.10")
        result = sortino_ratio(
            portfolio_return=portfolio_return,
            risk_free_rate=risk_free_rate,
            downside_deviation=downside_deviation,
        )
        assert_decimal_equal(actual=result, expected=Decimal("1.0000"))

    def test_sortino_ratio_high(self):
        """Test Sortino ratio with high downside-adjusted return."""
        portfolio_return = Decimal("0.18")
        risk_free_rate = Decimal("0.02")
        downside_deviation = Decimal("0.08")
        result = sortino_ratio(
            portfolio_return=portfolio_return,
            risk_free_rate=risk_free_rate,
            downside_deviation=downside_deviation,
        )
        assert_decimal_equal(actual=result, expected=Decimal("2.0000"))

    def test_sortino_ratio_zero_downside_deviation_raises_error(self):
        """Test that zero downside deviation raises error."""
        with pytest.raises(InvalidInputError):
            sortino_ratio(
                portfolio_return=Decimal("0.12"),
                risk_free_rate=Decimal("0.02"),
                downside_deviation=Decimal("0"),
            )


class TestValueAtRiskHistorical:
    """Test suite for value_at_risk_historical function."""

    def test_var_standard(self):
        """Test VaR calculation with standard inputs."""
        returns = [
            Decimal("-0.05"),
            Decimal("0.02"),
            Decimal("0.03"),
            Decimal("-0.01"),
            Decimal("0.04"),
        ]
        portfolio_value = Decimal("1000000")
        confidence_level = Decimal("0.95")
        result = value_at_risk_historical(
            returns=returns, portfolio_value=portfolio_value, confidence_level=confidence_level
        )
        # VaR should be positive loss amount
        assert result > 0

    def test_var_high_confidence(self):
        """Test VaR with high confidence level."""
        returns = [Decimal("-0.10"), Decimal("-0.05"), Decimal("0.02"), Decimal("0.01")]
        portfolio_value = Decimal("1000000")
        confidence_level = Decimal("0.99")
        result = value_at_risk_historical(
            returns=returns, portfolio_value=portfolio_value, confidence_level=confidence_level
        )
        assert result > Decimal("50000")  # Should capture worst loss

    def test_var_empty_returns_raises_error(self):
        """Test that empty returns raises error."""
        with pytest.raises(InvalidInputError):
            value_at_risk_historical(
                returns=[], portfolio_value=Decimal("1000000"), confidence_level=Decimal("0.95")
            )


class TestConditionalVaR:
    """Test suite for conditional_var function."""

    def test_cvar_standard(self):
        """Test CVaR calculation with standard inputs."""
        returns = [
            Decimal("-0.10"),
            Decimal("-0.05"),
            Decimal("0.02"),
            Decimal("0.01"),
            Decimal("-0.03"),
        ]
        portfolio_value = Decimal("1000000")
        confidence_level = Decimal("0.95")
        result = conditional_var(
            returns=returns, portfolio_value=portfolio_value, confidence_level=confidence_level
        )
        # CVaR should be positive and >= VaR
        assert result > 0

    def test_cvar_greater_than_var(self):
        """Test that CVaR is typically greater than or equal to VaR."""
        returns = [
            Decimal("-0.10"),
            Decimal("-0.08"),
            Decimal("-0.05"),
            Decimal("0.02"),
            Decimal("0.01"),
        ]
        portfolio_value = Decimal("1000000")
        confidence_level = Decimal("0.80")

        var = value_at_risk_historical(
            returns=returns, portfolio_value=portfolio_value, confidence_level=confidence_level
        )
        cvar = conditional_var(
            returns=returns, portfolio_value=portfolio_value, confidence_level=confidence_level
        )
        assert cvar >= var

    def test_cvar_empty_returns_raises_error(self):
        """Test that empty returns raises error."""
        with pytest.raises(InvalidInputError):
            conditional_var(
                returns=[], portfolio_value=Decimal("1000000"), confidence_level=Decimal("0.95")
            )


class TestMaximumDrawdown:
    """Test suite for maximum_drawdown function."""

    def test_maximum_drawdown_standard(self):
        """Test maximum drawdown with standard portfolio values."""
        values = [Decimal("100"), Decimal("110"), Decimal("105"), Decimal("95"), Decimal("100")]
        result = maximum_drawdown(values=values)
        # Peak = 110, Trough = 95, MDD = (110-95)/110 = 13.64%
        assert Decimal("13.00") < result < Decimal("14.00")

    def test_maximum_drawdown_no_decline(self):
        """Test maximum drawdown with no decline."""
        values = [Decimal("100"), Decimal("105"), Decimal("110"), Decimal("115")]
        result = maximum_drawdown(values=values)
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_maximum_drawdown_severe(self):
        """Test maximum drawdown with severe decline."""
        values = [Decimal("100"), Decimal("120"), Decimal("60"), Decimal("70")]
        result = maximum_drawdown(values=values)
        # Peak = 120, Trough = 60, MDD = (120-60)/120 = 50%
        assert_decimal_equal(actual=result, expected=Decimal("50.00"))

    def test_maximum_drawdown_multiple_peaks(self):
        """Test maximum drawdown with multiple peaks."""
        values = [Decimal("100"), Decimal("110"), Decimal("90"), Decimal("105"), Decimal("85")]
        result = maximum_drawdown(values=values)
        # Should capture worst drawdown
        assert result > Decimal("15.00")

    def test_maximum_drawdown_empty_raises_error(self):
        """Test that empty values raises error."""
        with pytest.raises(InvalidInputError):
            maximum_drawdown(values=[])
