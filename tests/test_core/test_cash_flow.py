"""Tests for cash flow metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.cash_flow import (
    cash_flow_margin,
    cash_flow_to_sales,
    cash_return_on_assets,
    free_cash_flow,
    free_cash_flow_to_equity,
    free_cash_flow_to_firm,
    operating_cash_flow,
    unlevered_free_cash_flow,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestFreeCashFlow:
    """Test suite for free_cash_flow function."""

    def test_fcf_positive(self):
        """Test FCF with positive cash flow."""
        operating_cf = Decimal("100000")
        capital_expenditures = Decimal("30000")
        result = free_cash_flow(
            operating_cash_flow=operating_cf, capital_expenditures=capital_expenditures
        )
        assert_decimal_equal(actual=result, expected=Decimal("70000.00"))

    def test_fcf_negative(self):
        """Test FCF can be negative when capex exceeds OCF."""
        operating_cf = Decimal("50000")
        capital_expenditures = Decimal("80000")
        result = free_cash_flow(
            operating_cash_flow=operating_cf, capital_expenditures=capital_expenditures
        )
        assert_decimal_equal(actual=result, expected=Decimal("-30000.00"))

    def test_fcf_zero_capex(self):
        """Test FCF with zero capital expenditures."""
        operating_cf = Decimal("100000")
        capital_expenditures = Decimal("0")
        result = free_cash_flow(
            operating_cash_flow=operating_cf, capital_expenditures=capital_expenditures
        )
        assert_decimal_equal(actual=result, expected=Decimal("100000.00"))


class TestOperatingCashFlow:
    """Test suite for operating_cash_flow function."""

    def test_ocf_standard(self):
        """Test OCF with standard inputs."""
        net_income = Decimal("50000")
        depreciation = Decimal("10000")
        amortization = Decimal("3000")
        working_capital_change = Decimal("-5000")
        result = operating_cash_flow(
            net_income=net_income,
            depreciation=depreciation,
            amortization=amortization,
            change_in_working_capital=working_capital_change,
        )
        # 50000 + 10000 + 3000 - (-5000) = 68000
        assert_decimal_equal(actual=result, expected=Decimal("68000.00"))

    def test_ocf_negative_wc_change(self):
        """Test OCF with positive working capital change (decrease in cash)."""
        net_income = Decimal("50000")
        depreciation = Decimal("10000")
        amortization = Decimal("2000")
        working_capital_change = Decimal("8000")
        result = operating_cash_flow(
            net_income=net_income,
            depreciation=depreciation,
            amortization=amortization,
            change_in_working_capital=working_capital_change,
        )
        # 50000 + 10000 + 2000 - 8000 = 54000
        assert_decimal_equal(actual=result, expected=Decimal("54000.00"))

    def test_ocf_zero_noncash_charges(self):
        """Test OCF with zero depreciation and amortization."""
        net_income = Decimal("50000")
        depreciation = Decimal("0")
        amortization = Decimal("0")
        working_capital_change = Decimal("0")
        result = operating_cash_flow(
            net_income=net_income,
            depreciation=depreciation,
            amortization=amortization,
            change_in_working_capital=working_capital_change,
        )
        assert_decimal_equal(actual=result, expected=Decimal("50000.00"))


class TestFreeCashFlowToEquity:
    """Test suite for free_cash_flow_to_equity function."""

    def test_fcfe_positive(self):
        """Test FCFE with positive result."""
        net_income = Decimal("100000")
        capex = Decimal("30000")
        depreciation = Decimal("20000")
        change_wc = Decimal("-5000")
        net_borrowing = Decimal("10000")
        result = free_cash_flow_to_equity(
            net_income=net_income,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
            net_borrowing=net_borrowing,
        )
        assert_decimal_equal(actual=result, expected=Decimal("105000.00"))

    def test_fcfe_with_debt_repayment(self):
        """Test FCFE with debt repayment (negative net borrowing)."""
        net_income = Decimal("100000")
        capex = Decimal("30000")
        depreciation = Decimal("20000")
        change_wc = Decimal("0")
        net_borrowing = Decimal("-15000")  # Debt repayment
        result = free_cash_flow_to_equity(
            net_income=net_income,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
            net_borrowing=net_borrowing,
        )
        assert_decimal_equal(actual=result, expected=Decimal("75000.00"))


class TestFreeCashFlowToFirm:
    """Test suite for free_cash_flow_to_firm function."""

    def test_fcff_positive(self):
        """Test FCFF with positive result."""
        ebit = Decimal("150000")
        tax_rate = Decimal("0.25")
        depreciation = Decimal("20000")
        capex = Decimal("30000")
        change_wc = Decimal("-5000")
        result = free_cash_flow_to_firm(
            ebit=ebit,
            tax_rate=tax_rate,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
        )
        # EBIT * (1 - 0.25) + 20000 - 30000 - (-5000) = 112500 + 20000 - 30000 + 5000 = 107500
        assert_decimal_equal(actual=result, expected=Decimal("107500.00"))

    def test_fcff_high_tax_rate(self):
        """Test FCFF with high tax rate."""
        ebit = Decimal("200000")
        tax_rate = Decimal("0.40")
        depreciation = Decimal("25000")
        capex = Decimal("40000")
        change_wc = Decimal("0")
        result = free_cash_flow_to_firm(
            ebit=ebit,
            tax_rate=tax_rate,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
        )
        # 200000 * (1 - 0.40) + 25000 - 40000 = 120000 + 25000 - 40000 = 105000
        assert_decimal_equal(actual=result, expected=Decimal("105000.00"))


class TestUnleveredFreeCashFlow:
    """Test suite for unlevered_free_cash_flow function."""

    def test_ufcf_standard(self):
        """Test unlevered FCF with standard inputs."""
        ebit = Decimal("100000")
        tax_rate = Decimal("0.30")
        depreciation = Decimal("15000")
        capex = Decimal("25000")
        change_wc = Decimal("-3000")
        result = unlevered_free_cash_flow(
            ebit=ebit,
            tax_rate=tax_rate,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
        )
        # 100000 * (1 - 0.30) + 15000 - 25000 - (-3000) = 70000 + 15000 - 25000 + 3000 = 63000
        assert_decimal_equal(actual=result, expected=Decimal("63000.00"))

    def test_ufcf_zero_tax(self):
        """Test unlevered FCF with zero tax rate."""
        ebit = Decimal("100000")
        tax_rate = Decimal("0")
        depreciation = Decimal("15000")
        capex = Decimal("25000")
        change_wc = Decimal("0")
        result = unlevered_free_cash_flow(
            ebit=ebit,
            tax_rate=tax_rate,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_wc,
        )
        assert_decimal_equal(actual=result, expected=Decimal("90000.00"))
