"""Tests for core depreciation functions."""

from decimal import Decimal

import pandas as pd
import pytest

from feconomics.core.depreciation import (
    book_value_at_year,
    composite_life,
    composite_rate,
    declining_balance_annual,
    depreciation_tax_shield,
    macrs_annual,
    straight_line_annual,
    sum_of_years_digits_annual,
    units_of_production_per_unit,
    units_of_production_period,
)
from feconomics.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestStraightLineAnnual:
    """Test suite for straight_line_annual function."""

    def test_straight_line_standard(self):
        """Test straight-line depreciation with standard inputs."""
        result = straight_line_annual(
            cost=Decimal("50000"), salvage_value=Decimal("5000"), useful_life=5
        )
        assert_decimal_equal(actual=result, expected=Decimal("9000.00"))

    def test_straight_line_zero_salvage(self):
        """Test straight-line with zero salvage value."""
        result = straight_line_annual(
            cost=Decimal("100000"), salvage_value=Decimal("0"), useful_life=10
        )
        assert_decimal_equal(actual=result, expected=Decimal("10000.00"))

    def test_straight_line_high_salvage(self):
        """Test straight-line with high salvage value."""
        result = straight_line_annual(
            cost=Decimal("50000"), salvage_value=Decimal("40000"), useful_life=5
        )
        assert_decimal_equal(actual=result, expected=Decimal("2000.00"))

    def test_straight_line_negative_cost_raises_error(self):
        """Test that negative cost raises error."""
        with pytest.raises(InvalidInputError):
            straight_line_annual(
                cost=Decimal("-50000"), salvage_value=Decimal("5000"), useful_life=5
            )

    def test_straight_line_zero_useful_life_raises_error(self):
        """Test that zero useful life raises error."""
        with pytest.raises(InvalidInputError):
            straight_line_annual(
                cost=Decimal("50000"), salvage_value=Decimal("5000"), useful_life=0
            )


class TestDecliningBalanceAnnual:
    """Test suite for declining_balance_annual function."""

    def test_declining_balance_double_declining(self):
        """Test double declining balance (factor 2.0)."""
        result = declining_balance_annual(
            book_value=Decimal("50000"), useful_life=5, factor=Decimal("2.0")
        )
        # Rate = 2/5 = 40%, so 50000 * 0.40 = 20000
        assert_decimal_equal(actual=result, expected=Decimal("20000.00"))

    def test_declining_balance_150_percent(self):
        """Test 150% declining balance."""
        result = declining_balance_annual(
            book_value=Decimal("30000"), useful_life=5, factor=Decimal("1.5")
        )
        # Rate = 1.5/5 = 30%, so 30000 * 0.30 = 9000
        assert_decimal_equal(actual=result, expected=Decimal("9000.00"))

    def test_declining_balance_low_book_value(self):
        """Test declining balance with low remaining book value."""
        result = declining_balance_annual(
            book_value=Decimal("5000"), useful_life=5, factor=Decimal("2.0")
        )
        assert_decimal_equal(actual=result, expected=Decimal("2000.00"))

    def test_declining_balance_negative_book_value_raises_error(self):
        """Test that negative book value raises error."""
        with pytest.raises(InvalidInputError):
            declining_balance_annual(
                book_value=Decimal("-10000"), useful_life=5, factor=Decimal("2.0")
            )

    def test_declining_balance_zero_useful_life_raises_error(self):
        """Test that zero useful life raises error."""
        with pytest.raises(InvalidInputError):
            declining_balance_annual(
                book_value=Decimal("50000"), useful_life=0, factor=Decimal("2.0")
            )


class TestSumOfYearsDigitsAnnual:
    """Test suite for sum_of_years_digits_annual function."""

    def test_sum_of_years_digits_first_year(self):
        """Test sum-of-years-digits for first year."""
        result = sum_of_years_digits_annual(
            cost=Decimal("50000"), salvage_value=Decimal("5000"), useful_life=5, year=1
        )
        # Depreciable base = 45000, SYD = 15, Year 1 fraction = 5/15
        # 45000 * (5/15) = 15000
        assert_decimal_equal(actual=result, expected=Decimal("15000.00"))

    def test_sum_of_years_digits_last_year(self):
        """Test sum-of-years-digits for last year."""
        result = sum_of_years_digits_annual(
            cost=Decimal("50000"), salvage_value=Decimal("5000"), useful_life=5, year=5
        )
        # Depreciable base = 45000, SYD = 15, Year 5 fraction = 1/15
        # 45000 * (1/15) = 3000
        assert_decimal_equal(actual=result, expected=Decimal("3000.00"))

    def test_sum_of_years_digits_middle_year(self):
        """Test sum-of-years-digits for middle year."""
        result = sum_of_years_digits_annual(
            cost=Decimal("60000"), salvage_value=Decimal("0"), useful_life=4, year=2
        )
        # Depreciable base = 60000, SYD = 10, Year 2 fraction = 3/10
        # 60000 * (3/10) = 18000
        assert_decimal_equal(actual=result, expected=Decimal("18000.00"))

    def test_sum_of_years_digits_invalid_year_raises_error(self):
        """Test that invalid year raises error."""
        with pytest.raises(InvalidInputError):
            sum_of_years_digits_annual(
                cost=Decimal("50000"), salvage_value=Decimal("5000"), useful_life=5, year=6
            )


class TestUnitsOfProductionPerUnit:
    """Test suite for units_of_production_per_unit function."""

    def test_units_of_production_per_unit_standard(self):
        """Test depreciation per unit calculation."""
        result = units_of_production_per_unit(
            cost=Decimal("100000"), salvage_value=Decimal("10000"), total_units=Decimal("50000")
        )
        # (100000 - 10000) / 50000 = 1.80 per unit
        assert_decimal_equal(actual=result, expected=Decimal("1.80"))

    def test_units_of_production_per_unit_zero_salvage(self):
        """Test units of production with zero salvage value."""
        result = units_of_production_per_unit(
            cost=Decimal("50000"), salvage_value=Decimal("0"), total_units=Decimal("10000")
        )
        assert_decimal_equal(actual=result, expected=Decimal("5.00"))

    def test_units_of_production_per_unit_high_units(self):
        """Test units of production with high unit count."""
        result = units_of_production_per_unit(
            cost=Decimal("200000"), salvage_value=Decimal("20000"), total_units=Decimal("1000000")
        )
        assert_decimal_equal(actual=result, expected=Decimal("0.18"))

    def test_units_of_production_zero_total_units_raises_error(self):
        """Test that zero total units raises error."""
        with pytest.raises(InvalidInputError):
            units_of_production_per_unit(
                cost=Decimal("100000"), salvage_value=Decimal("10000"), total_units=Decimal("0")
            )


class TestUnitsOfProductionPeriod:
    """Test suite for units_of_production_period function."""

    def test_units_of_production_period_standard(self):
        """Test period depreciation calculation."""
        result = units_of_production_period(
            cost=Decimal("100000"),
            salvage_value=Decimal("10000"),
            total_units=Decimal("50000"),
            units_produced=Decimal("5000"),
        )
        # Per unit = 1.80, so 5000 * 1.80 = 9000
        assert_decimal_equal(actual=result, expected=Decimal("9000.00"))

    def test_units_of_production_period_partial_use(self):
        """Test period depreciation with partial production."""
        result = units_of_production_period(
            cost=Decimal("50000"),
            salvage_value=Decimal("0"),
            total_units=Decimal("10000"),
            units_produced=Decimal("2500"),
        )
        # Per unit = 5.00, so 2500 * 5.00 = 12500
        assert_decimal_equal(actual=result, expected=Decimal("12500.00"))

    def test_units_of_production_period_low_production(self):
        """Test period depreciation with low production."""
        result = units_of_production_period(
            cost=Decimal("200000"),
            salvage_value=Decimal("20000"),
            total_units=Decimal("1000000"),
            units_produced=Decimal("10000"),
        )
        assert_decimal_equal(actual=result, expected=Decimal("1800.00"))


class TestMACRSAnnual:
    """Test suite for macrs_annual function."""

    def test_macrs_5_year_first_year(self):
        """Test MACRS 5-year property first year."""
        result = macrs_annual(cost=Decimal("10000"), recovery_period=5, year=1)
        # Year 1 rate for 5-year property is 20.00%
        assert_decimal_equal(actual=result, expected=Decimal("2000.00"))

    def test_macrs_5_year_second_year(self):
        """Test MACRS 5-year property second year."""
        result = macrs_annual(cost=Decimal("10000"), recovery_period=5, year=2)
        # Year 2 rate for 5-year property is 32.00%
        assert_decimal_equal(actual=result, expected=Decimal("3200.00"))

    def test_macrs_7_year_first_year(self):
        """Test MACRS 7-year property first year."""
        result = macrs_annual(cost=Decimal("50000"), recovery_period=7, year=1)
        # Year 1 rate for 7-year property is 14.29%
        assert_decimal_equal(actual=result, expected=Decimal("7145.00"))

    def test_macrs_3_year_property(self):
        """Test MACRS 3-year property."""
        result = macrs_annual(cost=Decimal("15000"), recovery_period=3, year=1)
        # Year 1 rate for 3-year property is 33.33%
        assert_decimal_equal(actual=result, expected=Decimal("4999.50"))

    def test_macrs_invalid_recovery_period_raises_error(self):
        """Test that invalid recovery period raises error."""
        with pytest.raises(InvalidInputError):
            macrs_annual(cost=Decimal("10000"), recovery_period=6, year=1)

    def test_macrs_invalid_year_raises_error(self):
        """Test that invalid year raises error."""
        with pytest.raises(InvalidInputError):
            macrs_annual(cost=Decimal("10000"), recovery_period=5, year=10)


class TestCompositeRate:
    """Test suite for composite_rate function."""

    def test_composite_rate_standard(self):
        """Test composite depreciation rate calculation."""
        costs = [Decimal("10000"), Decimal("20000"), Decimal("30000")]
        salvage_values = [Decimal("1000"), Decimal("2000"), Decimal("3000")]
        useful_lives = [5, 10, 15]

        result = composite_rate(
            asset_costs=costs, salvage_values=salvage_values, useful_lives=useful_lives
        )
        # Total depreciable = (9000 + 18000 + 27000) = 54000
        # Total cost = 60000
        # Composite rate = 54000 / (5*9000 + 10*18000 + 15*27000)
        # = 54000 / (45000 + 180000 + 405000) = 54000 / 630000
        assert result > Decimal("0") and result < Decimal("1")

    def test_composite_rate_equal_assets(self):
        """Test composite rate with equal assets."""
        costs = [Decimal("10000"), Decimal("10000")]
        salvage_values = [Decimal("0"), Decimal("0")]
        useful_lives = [5, 5]

        result = composite_rate(
            asset_costs=costs, salvage_values=salvage_values, useful_lives=useful_lives
        )
        # Should equal 1/5 = 0.20
        assert_decimal_equal(actual=result, expected=Decimal("0.20"))

    def test_composite_rate_mismatched_lengths_raises_error(self):
        """Test that mismatched array lengths raise error."""
        with pytest.raises(InvalidInputError):
            composite_rate(
                asset_costs=[Decimal("10000"), Decimal("20000")],
                salvage_values=[Decimal("1000")],
                useful_lives=[5, 10],
            )


class TestCompositeLife:
    """Test suite for composite_life function."""

    def test_composite_life_standard(self):
        """Test composite life calculation."""
        costs = [Decimal("10000"), Decimal("20000"), Decimal("30000")]
        salvage_values = [Decimal("1000"), Decimal("2000"), Decimal("3000")]
        useful_lives = [5, 10, 15]

        result = composite_life(
            asset_costs=costs, salvage_values=salvage_values, useful_lives=useful_lives
        )
        # Should be weighted average life
        assert result > Decimal("5") and result < Decimal("15")

    def test_composite_life_equal_assets(self):
        """Test composite life with equal assets."""
        costs = [Decimal("10000"), Decimal("10000")]
        salvage_values = [Decimal("0"), Decimal("0")]
        useful_lives = [10, 10]

        result = composite_life(
            asset_costs=costs, salvage_values=salvage_values, useful_lives=useful_lives
        )
        # Should equal 10 years
        assert_decimal_equal(actual=result, expected=Decimal("10.00"))

    def test_composite_life_varying_lives(self):
        """Test composite life with varying useful lives."""
        costs = [Decimal("30000"), Decimal("20000"), Decimal("10000")]
        salvage_values = [Decimal("0"), Decimal("0"), Decimal("0")]
        useful_lives = [15, 10, 5]

        result = composite_life(
            asset_costs=costs, salvage_values=salvage_values, useful_lives=useful_lives
        )
        # Weighted average should be closer to 15 (heaviest asset)
        assert result >= Decimal("10") and result <= Decimal("15")


class TestDepreciationTaxShield:
    """Test suite for depreciation_tax_shield function."""

    def test_tax_shield_standard(self):
        """Test depreciation tax shield calculation."""
        result = depreciation_tax_shield(
            depreciation_expense=Decimal("10000"), tax_rate=Decimal("0.25")
        )
        # Tax shield = 10000 * 0.25 = 2500
        assert_decimal_equal(actual=result, expected=Decimal("2500.00"))

    def test_tax_shield_high_depreciation(self):
        """Test tax shield with high depreciation."""
        result = depreciation_tax_shield(
            depreciation_expense=Decimal("100000"), tax_rate=Decimal("0.35")
        )
        assert_decimal_equal(actual=result, expected=Decimal("35000.00"))

    def test_tax_shield_low_tax_rate(self):
        """Test tax shield with low tax rate."""
        result = depreciation_tax_shield(
            depreciation_expense=Decimal("50000"), tax_rate=Decimal("0.15")
        )
        assert_decimal_equal(actual=result, expected=Decimal("7500.00"))

    def test_tax_shield_zero_depreciation(self):
        """Test tax shield with zero depreciation."""
        result = depreciation_tax_shield(
            depreciation_expense=Decimal("0"), tax_rate=Decimal("0.25")
        )
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_tax_shield_negative_depreciation_raises_error(self):
        """Test that negative depreciation raises error."""
        with pytest.raises(InvalidInputError):
            depreciation_tax_shield(
                depreciation_expense=Decimal("-10000"), tax_rate=Decimal("0.25")
            )


class TestBookValueAtYear:
    """Test suite for book_value_at_year function."""

    def test_book_value_standard(self):
        """Test book value calculation."""
        result = book_value_at_year(
            cost=Decimal("50000"), accumulated_depreciation=Decimal("20000")
        )
        assert_decimal_equal(actual=result, expected=Decimal("30000.00"))

    def test_book_value_fully_depreciated(self):
        """Test book value when fully depreciated."""
        result = book_value_at_year(
            cost=Decimal("50000"), accumulated_depreciation=Decimal("50000")
        )
        assert_decimal_equal(actual=result, expected=Decimal("0.00"))

    def test_book_value_minimal_depreciation(self):
        """Test book value with minimal depreciation."""
        result = book_value_at_year(
            cost=Decimal("100000"), accumulated_depreciation=Decimal("5000")
        )
        assert_decimal_equal(actual=result, expected=Decimal("95000.00"))

    def test_book_value_negative_cost_raises_error(self):
        """Test that negative cost raises error."""
        with pytest.raises(InvalidInputError):
            book_value_at_year(cost=Decimal("-50000"), accumulated_depreciation=Decimal("20000"))

    def test_book_value_negative_accumulated_raises_error(self):
        """Test that negative accumulated depreciation raises error."""
        with pytest.raises(InvalidInputError):
            book_value_at_year(cost=Decimal("50000"), accumulated_depreciation=Decimal("-20000"))
