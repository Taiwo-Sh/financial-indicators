"""Tests for banking industry metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.banking import (
    capital_adequacy_ratio,
    coverage_ratio,
    efficiency_ratio,
    loan_loss_provision_ratio,
    loan_to_deposit_ratio,
    net_interest_income,
    net_interest_margin,
    non_performing_loan_ratio,
    tier1_capital_ratio,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestNetInterestMargin:
    """Test suite for net_interest_margin function."""

    def test_nim_standard(self):
        """Test NIM with standard banking inputs."""
        nii = Decimal("50000000")  # $50M net interest income
        earning_assets = Decimal("1000000000")  # $1B earning assets
        result = net_interest_margin(nii, earning_assets)
        assert_decimal_equal(result, Decimal("5.00"))  # 5%

    def test_nim_high_margin(self):
        """Test NIM with high profitability."""
        nii = Decimal("80000000")
        earning_assets = Decimal("1000000000")
        result = net_interest_margin(nii, earning_assets)
        assert_decimal_equal(result, Decimal("8.00"))

    def test_nim_low_margin(self):
        """Test NIM with low profitability."""
        nii = Decimal("20000000")
        earning_assets = Decimal("1000000000")
        result = net_interest_margin(nii, earning_assets)
        assert_decimal_equal(result, Decimal("2.00"))

    def test_nim_zero_earning_assets_raises_error(self):
        """Test that zero earning assets raises error."""
        with pytest.raises(InvalidInputError):
            net_interest_margin(Decimal("50000000"), Decimal("0"))

    def test_nim_negative_earning_assets_raises_error(self):
        """Test that negative earning assets raises error."""
        with pytest.raises(InvalidInputError):
            net_interest_margin(Decimal("50000000"), Decimal("-1000000000"))


class TestNetInterestIncome:
    """Test suite for net_interest_income function."""

    def test_nii_positive(self):
        """Test NII with positive spread."""
        interest_income = Decimal("10000000")
        interest_expense = Decimal("4000000")
        result = net_interest_income(interest_income, interest_expense)
        assert_decimal_equal(result, Decimal("6000000.00"))

    def test_nii_narrow_spread(self):
        """Test NII with narrow interest spread."""
        interest_income = Decimal("5000000")
        interest_expense = Decimal("4500000")
        result = net_interest_income(interest_income, interest_expense)
        assert_decimal_equal(result, Decimal("500000.00"))

    def test_nii_negative(self):
        """Test NII can be negative when expenses exceed income."""
        interest_income = Decimal("3000000")
        interest_expense = Decimal("4000000")
        result = net_interest_income(interest_income, interest_expense)
        assert_decimal_equal(result, Decimal("-1000000.00"))

    def test_nii_negative_income_raises_error(self):
        """Test that negative interest income raises error."""
        with pytest.raises(InvalidInputError):
            net_interest_income(Decimal("-5000000"), Decimal("2000000"))


class TestEfficiencyRatio:
    """Test suite for efficiency_ratio function."""

    def test_efficiency_ratio_standard(self):
        """Test efficiency ratio with standard inputs."""
        non_interest_expense = Decimal("40000000")
        total_revenue = Decimal("100000000")
        result = efficiency_ratio(non_interest_expense, total_revenue)
        assert_decimal_equal(result, Decimal("40.00"))  # 40%

    def test_efficiency_ratio_efficient_bank(self):
        """Test efficiency ratio for efficient operations."""
        non_interest_expense = Decimal("25000000")
        total_revenue = Decimal("100000000")
        result = efficiency_ratio(non_interest_expense, total_revenue)
        assert_decimal_equal(result, Decimal("25.00"))

    def test_efficiency_ratio_inefficient_bank(self):
        """Test efficiency ratio for inefficient operations."""
        non_interest_expense = Decimal("70000000")
        total_revenue = Decimal("100000000")
        result = efficiency_ratio(non_interest_expense, total_revenue)
        assert_decimal_equal(result, Decimal("70.00"))

    def test_efficiency_ratio_zero_revenue_raises_error(self):
        """Test that zero revenue raises error."""
        with pytest.raises(InvalidInputError):
            efficiency_ratio(Decimal("40000000"), Decimal("0"))

    def test_efficiency_ratio_negative_expense_raises_error(self):
        """Test that negative expense raises error."""
        with pytest.raises(InvalidInputError):
            efficiency_ratio(Decimal("-40000000"), Decimal("100000000"))


class TestNonPerformingLoanRatio:
    """Test suite for non_performing_loan_ratio function."""

    def test_npl_ratio_low(self):
        """Test NPL ratio with low non-performing loans."""
        non_performing_loans = Decimal("2000000")
        total_loans = Decimal("100000000")
        result = non_performing_loan_ratio(non_performing_loans, total_loans)
        assert_decimal_equal(result, Decimal("2.00"))

    def test_npl_ratio_moderate(self):
        """Test NPL ratio with moderate credit risk."""
        non_performing_loans = Decimal("5000000")
        total_loans = Decimal("100000000")
        result = non_performing_loan_ratio(non_performing_loans, total_loans)
        assert_decimal_equal(result, Decimal("5.00"))

    def test_npl_ratio_high(self):
        """Test NPL ratio with high credit risk."""
        non_performing_loans = Decimal("10000000")
        total_loans = Decimal("100000000")
        result = non_performing_loan_ratio(non_performing_loans, total_loans)
        assert_decimal_equal(result, Decimal("10.00"))

    def test_npl_ratio_zero_total_loans_raises_error(self):
        """Test that zero total loans raises error."""
        with pytest.raises(InvalidInputError):
            non_performing_loan_ratio(Decimal("2000000"), Decimal("0"))

    def test_npl_ratio_negative_npl_raises_error(self):
        """Test that negative NPL raises error."""
        with pytest.raises(InvalidInputError):
            non_performing_loan_ratio(Decimal("-2000000"), Decimal("100000000"))


class TestLoanLossProvisionRatio:
    """Test suite for loan_loss_provision_ratio function."""

    def test_llp_ratio_standard(self):
        """Test LLP ratio with standard provisioning."""
        loan_loss_provisions = Decimal("1000000")
        total_loans = Decimal("100000000")
        result = loan_loss_provision_ratio(loan_loss_provisions, total_loans)
        assert_decimal_equal(result, Decimal("1.00"))

    def test_llp_ratio_conservative(self):
        """Test LLP ratio with conservative provisioning."""
        loan_loss_provisions = Decimal("3000000")
        total_loans = Decimal("100000000")
        result = loan_loss_provision_ratio(loan_loss_provisions, total_loans)
        assert_decimal_equal(result, Decimal("3.00"))

    def test_llp_ratio_zero_total_loans_raises_error(self):
        """Test that zero total loans raises error."""
        with pytest.raises(InvalidInputError):
            loan_loss_provision_ratio(Decimal("1000000"), Decimal("0"))

    def test_llp_ratio_negative_provision_raises_error(self):
        """Test that negative provision raises error."""
        with pytest.raises(InvalidInputError):
            loan_loss_provision_ratio(Decimal("-1000000"), Decimal("100000000"))


class TestCoverageRatio:
    """Test suite for coverage_ratio function."""

    def test_coverage_ratio_well_covered(self):
        """Test coverage ratio with adequate reserves."""
        loan_loss_reserves = Decimal("8000000")
        non_performing_loans = Decimal("5000000")
        result = coverage_ratio(loan_loss_reserves, non_performing_loans)
        assert_decimal_equal(result, Decimal("160.00"))  # 160%

    def test_coverage_ratio_exactly_covered(self):
        """Test coverage ratio at 100%."""
        loan_loss_reserves = Decimal("5000000")
        non_performing_loans = Decimal("5000000")
        result = coverage_ratio(loan_loss_reserves, non_performing_loans)
        assert_decimal_equal(result, Decimal("100.00"))

    def test_coverage_ratio_under_covered(self):
        """Test coverage ratio with insufficient reserves."""
        loan_loss_reserves = Decimal("3000000")
        non_performing_loans = Decimal("5000000")
        result = coverage_ratio(loan_loss_reserves, non_performing_loans)
        assert_decimal_equal(result, Decimal("60.00"))

    def test_coverage_ratio_zero_npl_raises_error(self):
        """Test that zero NPL raises error."""
        with pytest.raises(InvalidInputError):
            coverage_ratio(Decimal("8000000"), Decimal("0"))

    def test_coverage_ratio_negative_reserves_raises_error(self):
        """Test that negative reserves raise error."""
        with pytest.raises(InvalidInputError):
            coverage_ratio(Decimal("-8000000"), Decimal("5000000"))


class TestCapitalAdequacyRatio:
    """Test suite for capital_adequacy_ratio function."""

    def test_car_above_minimum(self):
        """Test CAR above Basel III minimum of 8%."""
        tier1_capital = Decimal("8000000")
        tier2_capital = Decimal("4000000")
        rwa = Decimal("100000000")
        result = capital_adequacy_ratio(tier1_capital, tier2_capital, rwa)
        assert_decimal_equal(result, Decimal("12.00"))

    def test_car_at_minimum(self):
        """Test CAR at Basel III minimum."""
        tier1_capital = Decimal("6000000")
        tier2_capital = Decimal("2000000")
        rwa = Decimal("100000000")
        result = capital_adequacy_ratio(tier1_capital, tier2_capital, rwa)
        assert_decimal_equal(result, Decimal("8.00"))

    def test_car_well_capitalized(self):
        """Test CAR for well-capitalized bank."""
        tier1_capital = Decimal("12000000")
        tier2_capital = Decimal("6000000")
        rwa = Decimal("100000000")
        result = capital_adequacy_ratio(tier1_capital, tier2_capital, rwa)
        assert_decimal_equal(result, Decimal("18.00"))

    def test_car_zero_rwa_raises_error(self):
        """Test that zero RWA raises error."""
        with pytest.raises(InvalidInputError):
            capital_adequacy_ratio(Decimal("8000000"), Decimal("4000000"), Decimal("0"))

    def test_car_negative_capital_raises_error(self):
        """Test that negative capital raises error."""
        with pytest.raises(InvalidInputError):
            capital_adequacy_ratio(Decimal("-8000000"), Decimal("4000000"), Decimal("100000000"))


class TestTier1CapitalRatio:
    """Test suite for tier1_capital_ratio function."""

    def test_tier1_above_minimum(self):
        """Test Tier 1 ratio above Basel III minimum of 6%."""
        tier1_capital = Decimal("8000000")
        rwa = Decimal("100000000")
        result = tier1_capital_ratio(tier1_capital, rwa)
        assert_decimal_equal(result, Decimal("8.00"))

    def test_tier1_at_minimum(self):
        """Test Tier 1 ratio at Basel III minimum."""
        tier1_capital = Decimal("6000000")
        rwa = Decimal("100000000")
        result = tier1_capital_ratio(tier1_capital, rwa)
        assert_decimal_equal(result, Decimal("6.00"))

    def test_tier1_strong_capital(self):
        """Test Tier 1 ratio with strong capital position."""
        tier1_capital = Decimal("15000000")
        rwa = Decimal("100000000")
        result = tier1_capital_ratio(tier1_capital, rwa)
        assert_decimal_equal(result, Decimal("15.00"))

    def test_tier1_zero_rwa_raises_error(self):
        """Test that zero RWA raises error."""
        with pytest.raises(InvalidInputError):
            tier1_capital_ratio(Decimal("8000000"), Decimal("0"))

    def test_tier1_negative_capital_raises_error(self):
        """Test that negative Tier 1 capital raises error."""
        with pytest.raises(InvalidInputError):
            tier1_capital_ratio(Decimal("-8000000"), Decimal("100000000"))


class TestLoanToDepositRatio:
    """Test suite for loan_to_deposit_ratio function."""

    def test_ltd_moderate(self):
        """Test LTD ratio at moderate level."""
        total_loans = Decimal("80000000")
        total_deposits = Decimal("100000000")
        result = loan_to_deposit_ratio(total_loans, total_deposits)
        assert_decimal_equal(result, Decimal("80.00"))

    def test_ltd_conservative(self):
        """Test LTD ratio for conservative lending."""
        total_loans = Decimal("60000000")
        total_deposits = Decimal("100000000")
        result = loan_to_deposit_ratio(total_loans, total_deposits)
        assert_decimal_equal(result, Decimal("60.00"))

    def test_ltd_aggressive(self):
        """Test LTD ratio for aggressive lending."""
        total_loans = Decimal("95000000")
        total_deposits = Decimal("100000000")
        result = loan_to_deposit_ratio(total_loans, total_deposits)
        assert_decimal_equal(result, Decimal("95.00"))

    def test_ltd_over_100(self):
        """Test LTD ratio exceeding 100% (borrowing from other sources)."""
        total_loans = Decimal("120000000")
        total_deposits = Decimal("100000000")
        result = loan_to_deposit_ratio(total_loans, total_deposits)
        assert_decimal_equal(result, Decimal("120.00"))

    def test_ltd_zero_deposits_raises_error(self):
        """Test that zero deposits raises error."""
        with pytest.raises(InvalidInputError):
            loan_to_deposit_ratio(Decimal("80000000"), Decimal("0"))

    def test_ltd_negative_loans_raises_error(self):
        """Test that negative loans raise error."""
        with pytest.raises(InvalidInputError):
            loan_to_deposit_ratio(Decimal("-80000000"), Decimal("100000000"))
