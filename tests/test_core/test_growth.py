"""Tests for growth metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.growth import (
    compound_annual_growth_rate,
    earnings_growth_rate,
    retention_ratio,
    revenue_growth_rate,
    sustainable_growth_rate,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestRevenueGrowthRate:
    """Test suite for revenue_growth_rate function."""

    def test_revenue_growth_positive(self):
        """Test revenue growth with positive growth."""
        revenue_current = Decimal("1200000")
        revenue_previous = Decimal("1000000")
        result = revenue_growth_rate(
            revenue_current=revenue_current, revenue_previous=revenue_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("20.00"))

    def test_revenue_growth_negative(self):
        """Test revenue growth with decline."""
        revenue_current = Decimal("900000")
        revenue_previous = Decimal("1000000")
        result = revenue_growth_rate(
            revenue_current=revenue_current, revenue_previous=revenue_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("-10.00"))

    def test_revenue_growth_zero(self):
        """Test revenue growth with no change."""
        revenue_current = Decimal("1000000")
        revenue_previous = Decimal("1000000")
        result = revenue_growth_rate(
            revenue_current=revenue_current, revenue_previous=revenue_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_revenue_growth_zero_previous_raises_error(self):
        """Test that zero previous revenue raises error."""
        with pytest.raises(InvalidInputError):
            revenue_growth_rate(revenue_current=Decimal("1200000"), revenue_previous=Decimal("0"))


class TestEarningsGrowthRate:
    """Test suite for earnings_growth_rate function."""

    def test_earnings_growth_positive(self):
        """Test earnings growth with positive growth."""
        earnings_current = Decimal("150000")
        earnings_previous = Decimal("120000")
        result = earnings_growth_rate(
            earnings_current=earnings_current, earnings_previous=earnings_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("25.00"))

    def test_earnings_growth_negative(self):
        """Test earnings growth with decline."""
        earnings_current = Decimal("100000")
        earnings_previous = Decimal("120000")
        result = earnings_growth_rate(
            earnings_current=earnings_current, earnings_previous=earnings_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("-16.67"))

    def test_earnings_growth_large_increase(self):
        """Test earnings growth with large increase."""
        earnings_current = Decimal("300000")
        earnings_previous = Decimal("100000")
        result = earnings_growth_rate(
            earnings_current=earnings_current, earnings_previous=earnings_previous
        )
        assert_decimal_equal(actual=result, expected=Decimal("200.00"))

    def test_earnings_growth_zero_previous_raises_error(self):
        """Test that zero previous earnings raises error."""
        with pytest.raises(InvalidInputError):
            earnings_growth_rate(earnings_current=Decimal("150000"), earnings_previous=Decimal("0"))


class TestCompoundAnnualGrowthRate:
    """Test suite for compound_annual_growth_rate function."""

    def test_cagr_positive_growth(self):
        """Test CAGR with positive growth."""
        ending_value = Decimal("1500000")
        beginning_value = Decimal("1000000")
        num_years = 3
        result = compound_annual_growth_rate(
            ending_value=ending_value, beginning_value=beginning_value, num_years=num_years
        )
        # CAGR = (1500000/1000000)^(1/3) - 1 = 0.1447... = 14.47%
        assert Decimal("14.00") < result < Decimal("15.00")

    def test_cagr_negative_growth(self):
        """Test CAGR with negative growth."""
        ending_value = Decimal("800000")
        beginning_value = Decimal("1000000")
        num_years = 2
        result = compound_annual_growth_rate(
            ending_value=ending_value, beginning_value=beginning_value, num_years=num_years
        )
        assert result < 0  # Should be negative

    def test_cagr_one_year(self):
        """Test CAGR with one year period."""
        ending_value = Decimal("1200000")
        beginning_value = Decimal("1000000")
        num_years = 1
        result = compound_annual_growth_rate(
            ending_value=ending_value, beginning_value=beginning_value, num_years=num_years
        )
        assert_decimal_equal(actual=result, expected=Decimal("20.00"))

    def test_cagr_zero_beginning_value_raises_error(self):
        """Test that zero beginning value raises error."""
        with pytest.raises(InvalidInputError):
            compound_annual_growth_rate(
                ending_value=Decimal("1500000"), beginning_value=Decimal("0"), num_years=3
            )

    def test_cagr_zero_years_raises_error(self):
        """Test that zero years raises error."""
        with pytest.raises(InvalidInputError):
            compound_annual_growth_rate(
                ending_value=Decimal("1500000"), beginning_value=Decimal("1000000"), num_years=0
            )

    def test_cagr_negative_years_raises_error(self):
        """Test that negative years raises error."""
        with pytest.raises(InvalidInputError):
            compound_annual_growth_rate(
                ending_value=Decimal("1500000"), beginning_value=Decimal("1000000"), num_years=-1
            )


class TestSustainableGrowthRate:
    """Test suite for sustainable_growth_rate function."""

    def test_sgr_standard(self):
        """Test sustainable growth rate with standard inputs."""
        roe = Decimal("0.15")  # 15%
        dividend_payout_ratio = Decimal("0.40")  # 40%
        result = sustainable_growth_rate(roe=roe, dividend_payout_ratio=dividend_payout_ratio)
        assert_decimal_equal(actual=result, expected=Decimal("9.00"))

    def test_sgr_no_dividends(self):
        """Test SGR with no dividend payout."""
        roe = Decimal("0.20")
        dividend_payout_ratio = Decimal("0")
        result = sustainable_growth_rate(roe=roe, dividend_payout_ratio=dividend_payout_ratio)
        assert_decimal_equal(actual=result, expected=Decimal("20.00"))

    def test_sgr_all_dividends(self):
        """Test SGR with 100% dividend payout."""
        roe = Decimal("0.15")
        dividend_payout_ratio = Decimal("1.00")
        result = sustainable_growth_rate(roe=roe, dividend_payout_ratio=dividend_payout_ratio)
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_sgr_high_roe(self):
        """Test SGR with high ROE."""
        roe = Decimal("0.25")
        dividend_payout_ratio = Decimal("0.30")
        result = sustainable_growth_rate(roe=roe, dividend_payout_ratio=dividend_payout_ratio)
        assert_decimal_equal(actual=result, expected=Decimal("17.50"))


class TestRetentionRatio:
    """Test suite for retention_ratio function."""

    def test_retention_ratio_standard(self):
        """Test retention ratio with standard inputs."""
        dividends = Decimal("40000")
        net_income = Decimal("100000")
        result = retention_ratio(dividends=dividends, net_income=net_income)
        assert_decimal_equal(actual=result, expected=Decimal("0.6000"))

    def test_retention_ratio_no_dividends(self):
        """Test retention ratio with no dividends."""
        dividends = Decimal("0")
        net_income = Decimal("100000")
        result = retention_ratio(dividends=dividends, net_income=net_income)
        assert_decimal_equal(actual=result, expected=Decimal("1.0000"))

    def test_retention_ratio_all_dividends(self):
        """Test retention ratio with all earnings paid as dividends."""
        dividends = Decimal("100000")
        net_income = Decimal("100000")
        result = retention_ratio(dividends=dividends, net_income=net_income)
        assert_decimal_equal(actual=result, expected=Decimal("0.0000"))

    def test_retention_ratio_high_retention(self):
        """Test retention ratio with high retention."""
        dividends = Decimal("20000")
        net_income = Decimal("100000")
        result = retention_ratio(dividends=dividends, net_income=net_income)
        assert_decimal_equal(actual=result, expected=Decimal("0.8000"))

    def test_retention_ratio_zero_income_raises_error(self):
        """Test that zero net income raises error."""
        with pytest.raises(InvalidInputError):
            retention_ratio(dividends=Decimal("40000"), net_income=Decimal("0"))
