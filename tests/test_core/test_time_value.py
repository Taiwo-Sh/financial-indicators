"""Tests for core time value functions."""

from decimal import Decimal

import pytest

from financial_indicators.core.time_value import (
    annuity_present_value,
    discounted_payback_period,
    future_value,
    internal_rate_of_return,
    net_present_value,
    payback_period,
    present_value,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestNetPresentValue:
    """Test suite for net_present_value function."""

    def test_npv_positive_cash_flows(self):
        """Test NPV with positive cash flows after initial investment."""
        cash_flows = [
            Decimal("-1000"),
            Decimal("500"),
            Decimal("500"),
            Decimal("500"),
        ]
        discount_rate = Decimal("0.1")
        result = net_present_value(cash_flows, discount_rate)
        # Expected: approximately 243.43
        assert_decimal_equal(result, Decimal("243.43"))

    def test_npv_zero_discount_rate(self):
        """Test NPV with zero discount rate (simple sum)."""
        cash_flows = [Decimal("-1000"), Decimal("500"), Decimal("500")]
        discount_rate = Decimal("0")
        result = net_present_value(cash_flows, discount_rate)
        assert_decimal_equal(result, Decimal("0.00"))

    def test_npv_high_discount_rate(self):
        """Test NPV with high discount rate."""
        cash_flows = [Decimal("-1000"), Decimal("600"), Decimal("600")]
        discount_rate = Decimal("0.5")
        result = net_present_value(cash_flows, discount_rate)
        assert result < 0  # Should be negative

    def test_npv_negative_discount_rate_raises_error(self):
        """Test that negative discount rate raises error."""
        cash_flows = [Decimal("-1000"), Decimal("500")]
        discount_rate = Decimal("-0.1")
        with pytest.raises(InvalidInputError):
            net_present_value(cash_flows, discount_rate)

    def test_npv_empty_cash_flows_raises_error(self):
        """Test that empty cash flows raises error."""
        with pytest.raises(InvalidInputError):
            net_present_value([], Decimal("0.1"))


class TestInternalRateOfReturn:
    """Test suite for internal_rate_of_return function."""

    def test_irr_standard_investment(self):
        """Test IRR with standard investment cash flows."""
        cash_flows = [
            Decimal("-1000"),
            Decimal("500"),
            Decimal("500"),
            Decimal("500"),
        ]
        result = internal_rate_of_return(cash_flows)
        assert result is not None
        # IRR should be around 23%
        assert Decimal("0.20") < result < Decimal("0.30")

    def test_irr_no_sign_change_returns_none(self):
        """Test that IRR returns None when no sign changes."""
        cash_flows = [100, Decimal("200"), Decimal("300")]
        result = internal_rate_of_return(cash_flows)
        assert result is None

    def test_irr_all_negative_returns_none(self):
        """Test that IRR returns None for all negative cash flows."""
        cash_flows = [Decimal("-100"), Decimal("-200"), Decimal("-300")]
        result = internal_rate_of_return(cash_flows)
        assert result is None

    def test_irr_empty_cash_flows_raises_error(self):
        """Test that empty cash flows raises error."""
        with pytest.raises(InvalidInputError):
            internal_rate_of_return([])


class TestPresentValue:
    """Test suite for present_value function."""

    def test_pv_standard_calculation(self):
        """Test present value with standard inputs."""
        fv = Decimal("1000")
        rate = Decimal("0.05")
        periods = 5
        result = present_value(fv, rate, periods)
        expected = Decimal("783.53")
        assert_decimal_equal(result, expected)

    def test_pv_zero_periods(self):
        """Test present value with zero periods."""
        fv = Decimal("1000")
        rate = Decimal("0.05")
        periods = 0
        result = present_value(fv, rate, periods)
        assert_decimal_equal(result, fv)

    def test_pv_negative_rate_raises_error(self):
        """Test that negative rate raises error."""
        with pytest.raises(InvalidInputError):
            present_value(Decimal("1000"), Decimal("-0.05"), 5)

    def test_pv_negative_periods_raises_error(self):
        """Test that negative periods raises error."""
        with pytest.raises(InvalidInputError):
            present_value(Decimal("1000"), Decimal("0.05"), -1)


class TestFutureValue:
    """Test suite for future_value function."""

    def test_fv_standard_calculation(self):
        """Test future value with standard inputs."""
        pv = Decimal("1000")
        rate = Decimal("0.05")
        periods = 5
        result = future_value(pv, rate, periods)
        expected = Decimal("1276.28")
        assert_decimal_equal(result, expected)

    def test_fv_zero_rate(self):
        """Test future value with zero rate."""
        pv = Decimal("1000")
        rate = Decimal("0")
        periods = 5
        result = future_value(pv, rate, periods)
        assert_decimal_equal(result, pv)

    def test_fv_negative_rate_raises_error(self):
        """Test that negative rate raises error."""
        with pytest.raises(InvalidInputError):
            future_value(Decimal("1000"), Decimal("-0.05"), 5)


class TestAnnuityPresentValue:
    """Test suite for annuity_present_value function."""

    def test_annuity_pv_standard(self):
        """Test annuity present value calculation."""
        payment = Decimal("100")
        rate = Decimal("0.05")
        periods = 10
        result = annuity_present_value(payment, rate, periods)
        expected = Decimal("772.17")
        assert abs(result - expected) < Decimal("0.10")

    def test_annuity_pv_zero_rate_raises_error(self):
        """Test that zero rate raises error."""
        with pytest.raises(InvalidInputError):
            annuity_present_value(Decimal("100"), Decimal("0"), 10)


class TestPaybackPeriod:
    """Test suite for payback_period function."""

    def test_payback_period_standard(self):
        """Test payback period with standard cash flows."""
        cash_flows = [
            Decimal("-1000"),
            Decimal("300"),
            Decimal("400"),
            Decimal("500"),
        ]
        result = payback_period(cash_flows)
        assert result is not None
        # Should payback between 2 and 3 years
        assert Decimal("2") < result < Decimal("3")

    def test_payback_period_never_returns_none(self):
        """Test that payback period returns None when never paid back."""
        cash_flows = [Decimal("-1000"), 100, 100]
        result = payback_period(cash_flows)
        assert result is None

    def test_payback_period_immediate(self):
        """Test payback period with immediate recovery."""
        cash_flows = [Decimal("-1000"), Decimal("2000")]
        result = payback_period(cash_flows)
        assert result is not None
        assert_decimal_equal(result, Decimal("0.50"))  # Recovers in 0.5 years


class TestDiscountedPaybackPeriod:
    """Test suite for discounted_payback_period function."""

    def test_discounted_payback_standard(self):
        """Test discounted payback period."""
        cash_flows = [
            Decimal("-1000"),
            Decimal("500"),
            Decimal("500"),
            Decimal("500"),
        ]
        rate = Decimal("0.1")
        result = discounted_payback_period(cash_flows, rate)
        assert result is not None  # Should recover with higher cash flows
        # Should be between 2 and 3 years (around 2.35 years with 10% discount rate)
        assert Decimal("2.0") < result < Decimal("3.0")

    def test_discounted_payback_negative_rate_raises_error(self):
        """Test that negative rate raises error."""
        cash_flows = [Decimal("-1000"), Decimal("500"), Decimal("500")]
        with pytest.raises(InvalidInputError):
            discounted_payback_period(cash_flows, Decimal("-0.1"))
