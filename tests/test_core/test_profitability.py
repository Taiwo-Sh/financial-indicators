"""Tests for profitability metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.profitability import (
    ebit,
    ebitda,
    economic_value_added,
    gross_profit_margin,
    net_profit_margin,
    operating_profit_margin,
    profitability_index,
    return_on_assets,
    return_on_equity,
    return_on_investment,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestReturnOnInvestment:
    """Test suite for return_on_investment function."""

    def test_roi_positive_return(self):
        """Test ROI with positive return."""
        net_profit = Decimal("500")
        investment = Decimal("2000")
        result = return_on_investment(net_profit, investment)
        assert_decimal_equal(result, Decimal("25.00"))

    def test_roi_negative_return(self):
        """Test ROI with negative return (loss)."""
        net_profit = Decimal("-200")
        investment = Decimal("1000")
        result = return_on_investment(net_profit, investment)
        assert_decimal_equal(result, Decimal("-20.00"))

    def test_roi_zero_investment_raises_error(self):
        """Test that zero investment raises error."""
        with pytest.raises(InvalidInputError):
            return_on_investment(Decimal("100"), Decimal("0"))


class TestReturnOnAssets:
    """Test suite for return_on_assets function."""

    def test_roa_standard(self):
        """Test ROA with standard inputs."""
        net_income = Decimal("50000")
        total_assets = Decimal("500000")
        result = return_on_assets(net_income, total_assets)
        assert_decimal_equal(result, Decimal("10.00"))

    def test_roa_negative_assets_raises_error(self):
        """Test that negative assets raises error."""
        with pytest.raises(InvalidInputError):
            return_on_assets(Decimal("50000"), Decimal("-500000"))


class TestReturnOnEquity:
    """Test suite for return_on_equity function."""

    def test_roe_standard(self):
        """Test ROE with standard inputs."""
        net_income = Decimal("50000")
        equity = Decimal("250000")
        result = return_on_equity(net_income, equity)
        assert_decimal_equal(result, Decimal("20.00"))

    def test_roe_zero_equity_raises_error(self):
        """Test that zero equity raises error."""
        with pytest.raises(InvalidInputError):
            return_on_equity(Decimal("50000"), Decimal("0"))


class TestGrossProfitMargin:
    """Test suite for gross_profit_margin function."""

    def test_gpm_standard(self):
        """Test gross profit margin."""
        gross_profit = Decimal("400000")
        revenue = Decimal("1000000")
        result = gross_profit_margin(gross_profit, revenue)
        assert_decimal_equal(result, Decimal("40.00"))

    def test_gpm_zero_revenue_raises_error(self):
        """Test that zero revenue raises error."""
        with pytest.raises(InvalidInputError):
            gross_profit_margin(Decimal("400000"), Decimal("0"))


class TestOperatingProfitMargin:
    """Test suite for operating_profit_margin function."""

    def test_opm_standard(self):
        """Test operating profit margin."""
        operating_income = Decimal("200000")
        revenue = Decimal("1000000")
        result = operating_profit_margin(operating_income, revenue)
        assert_decimal_equal(result, Decimal("20.00"))


class TestNetProfitMargin:
    """Test suite for net_profit_margin function."""

    def test_npm_standard(self):
        """Test net profit margin."""
        net_income = Decimal("100000")
        revenue = Decimal("1000000")
        result = net_profit_margin(net_income, revenue)
        assert_decimal_equal(result, Decimal("10.00"))

    def test_npm_negative_margin(self):
        """Test net profit margin with loss."""
        net_income = Decimal("-50000")
        revenue = Decimal("1000000")
        result = net_profit_margin(net_income, revenue)
        assert_decimal_equal(result, Decimal("-5.00"))


class TestEBITDA:
    """Test suite for ebitda function."""

    def test_ebitda_standard(self):
        """Test EBITDA calculation."""
        net_income = Decimal("100000")
        interest = Decimal("20000")
        taxes = Decimal("30000")
        depreciation = Decimal("40000")
        amortization = Decimal("10000")
        result = ebitda(net_income, interest, taxes, depreciation, amortization)
        assert_decimal_equal(result, Decimal("200000.00"))

    def test_ebitda_zero_da(self):
        """Test EBITDA with zero depreciation and amortization."""
        net_income = Decimal("100000")
        interest = Decimal("20000")
        taxes = Decimal("30000")
        depreciation = Decimal("0")
        amortization = Decimal("0")
        result = ebitda(net_income, interest, taxes, depreciation, amortization)
        assert_decimal_equal(result, Decimal("150000.00"))


class TestEBIT:
    """Test suite for ebit function."""

    def test_ebit_standard(self):
        """Test EBIT calculation."""
        revenue = Decimal("1000000")
        cogs = Decimal("600000")
        opex = Decimal("200000")
        result = ebit(revenue, cogs, opex)
        assert_decimal_equal(result, Decimal("200000.00"))


class TestProfitabilityIndex:
    """Test suite for profitability_index function."""

    def test_pi_greater_than_one(self):
        """Test PI with profitable project."""
        pv_cash_flows = Decimal("1200000")
        investment = Decimal("1000000")
        result = profitability_index(pv_cash_flows, investment)
        assert_decimal_equal(result, Decimal("1.2000"))

    def test_pi_less_than_one(self):
        """Test PI with unprofitable project."""
        pv_cash_flows = Decimal("800000")
        investment = Decimal("1000000")
        result = profitability_index(pv_cash_flows, investment)
        assert_decimal_equal(result, Decimal("0.8000"))

    def test_pi_zero_investment_raises_error(self):
        """Test that zero investment raises error."""
        with pytest.raises(InvalidInputError):
            profitability_index(Decimal("1200000"), Decimal("0"))


class TestEconomicValueAdded:
    """Test suite for economic_value_added function."""

    def test_eva_positive(self):
        """Test EVA with positive value creation."""
        nopat = Decimal("500000")
        capital = Decimal("2000000")
        wacc = Decimal("0.12")
        result = economic_value_added(nopat, capital, wacc)
        assert_decimal_equal(result, Decimal("260000.00"))

    def test_eva_negative(self):
        """Test EVA with value destruction."""
        nopat = Decimal("200000")
        capital = Decimal("2000000")
        wacc = Decimal("0.12")
        result = economic_value_added(nopat, capital, wacc)
        assert_decimal_equal(result, Decimal("-40000.00"))

    def test_eva_zero_capital_raises_error(self):
        """Test that zero capital raises error."""
        with pytest.raises(InvalidInputError):
            economic_value_added(Decimal("500000"), Decimal("0"), Decimal("0.12"))
