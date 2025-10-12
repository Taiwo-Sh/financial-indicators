"""Tests for petroleum economics metrics."""

from decimal import Decimal

import pytest

from financial_indicators.core.petroleum import (
    breakeven_price,
    capital_efficiency,
    finding_development_cost,
    lifting_cost,
    netback,
    operating_netback_margin,
    recycle_ratio,
    reserve_life_index,
    reserve_replacement_ratio,
    reserves_per_share,
)
from financial_indicators.exceptions import InvalidInputError
from tests.conftest import assert_decimal_equal


class TestFindingDevelopmentCost:
    """Test suite for finding_development_cost function."""

    def test_fdc_standard_calculation(self):
        """Test F&D cost with standard inputs."""
        exploration = Decimal("20000000")  # $20M exploration
        development = Decimal("30000000")  # $30M development
        reserves = Decimal("5000000")  # 5M BOE
        result = finding_development_cost(exploration, development, reserves)
        assert_decimal_equal(result, Decimal("10.00"))  # $10/BOE

    def test_fdc_high_cost(self):
        """Test F&D cost with high exploration costs."""
        exploration = Decimal("50000000")
        development = Decimal("50000000")
        reserves = Decimal("2000000")
        result = finding_development_cost(exploration, development, reserves)
        assert_decimal_equal(result, Decimal("50.00"))

    def test_fdc_zero_reserves_raises_error(self):
        """Test that zero reserves raises error."""
        with pytest.raises(InvalidInputError):
            finding_development_cost(Decimal("500000"), Decimal("500000"), Decimal("0"))

    def test_fdc_negative_reserves_raises_error(self):
        """Test that negative reserves raises error."""
        with pytest.raises(InvalidInputError):
            finding_development_cost(Decimal("500000"), Decimal("500000"), Decimal("-1000000"))


class TestReserveReplacementRatio:
    """Test suite for reserve_replacement_ratio function."""

    def test_rrr_above_100_percent(self):
        """Test RRR with reserves added exceeding production."""
        reserves_added = Decimal("1200000")
        production = Decimal("1000000")
        result = reserve_replacement_ratio(reserves_added, production)
        assert_decimal_equal(result, Decimal("1.20"))  # Ratio of 1.20 (120%)

    def test_rrr_exactly_100_percent(self):
        """Test RRR with reserves equal to production."""
        reserves_added = Decimal("1000000")
        production = Decimal("1000000")
        result = reserve_replacement_ratio(reserves_added, production)
        assert_decimal_equal(result, Decimal("1.00"))  # Ratio of 1.00 (100%)

    def test_rrr_below_100_percent(self):
        """Test RRR with insufficient reserve replacement."""
        reserves_added = Decimal("800000")
        production = Decimal("1000000")
        result = reserve_replacement_ratio(reserves_added, production)
        assert_decimal_equal(result, Decimal("0.80"))  # Ratio of 0.80 (80%)

    def test_rrr_zero_production_raises_error(self):
        """Test that zero production raises error."""
        with pytest.raises(InvalidInputError):
            reserve_replacement_ratio(Decimal("1000000"), Decimal("0"))


class TestReserveLifeIndex:
    """Test suite for reserve_life_index function."""

    def test_rli_standard_calculation(self):
        """Test RLI with standard inputs."""
        proven_reserves = Decimal("10000000")  # 10M BOE
        annual_production = Decimal("1000000")  # 1M BOE/year
        result = reserve_life_index(proven_reserves, annual_production)
        assert_decimal_equal(result, Decimal("10.00"))  # 10 years

    def test_rli_depleting_reserves(self):
        """Test RLI with high production rate."""
        proven_reserves = Decimal("5000000")
        annual_production = Decimal("2000000")
        result = reserve_life_index(proven_reserves, annual_production)
        assert_decimal_equal(result, Decimal("2.50"))

    def test_rli_zero_production_raises_error(self):
        """Test that zero production raises error."""
        with pytest.raises(InvalidInputError):
            reserve_life_index(Decimal("1000000"), Decimal("0"))

    def test_rli_negative_reserves_raises_error(self):
        """Test that negative reserves raises error."""
        with pytest.raises(InvalidInputError):
            reserve_life_index(Decimal("-1000000"), Decimal("100000"))


class TestReservesPerShare:
    """Test suite for reserves_per_share function."""

    def test_rps_standard_calculation(self):
        """Test reserves per share with standard inputs."""
        proven_reserves = Decimal("50000000")  # 50M BOE
        shares_outstanding = Decimal("10000000")  # 10M shares
        result = reserves_per_share(proven_reserves, shares_outstanding)
        assert_decimal_equal(result, Decimal("5.00"))

    def test_rps_low_reserves(self):
        """Test RPS with low reserves relative to shares."""
        proven_reserves = Decimal("1000000")
        shares_outstanding = Decimal("5000000")
        result = reserves_per_share(proven_reserves, shares_outstanding)
        assert_decimal_equal(result, Decimal("0.20"))

    def test_rps_zero_shares_raises_error(self):
        """Test that zero shares raises error."""
        with pytest.raises(InvalidInputError):
            reserves_per_share(Decimal("1000000"), Decimal("0"))


class TestLiftingCost:
    """Test suite for lifting_cost function."""

    def test_lifting_cost_standard(self):
        """Test lifting cost with standard inputs."""
        operating_costs = Decimal("20000000")  # $20M
        production = Decimal("2000000")  # 2M BOE
        result = lifting_cost(operating_costs, production)
        assert_decimal_equal(result, Decimal("10.00"))  # $10/BOE

    def test_lifting_cost_low_efficiency(self):
        """Test lifting cost with high operating costs."""
        operating_costs = Decimal("50000000")
        production = Decimal("1000000")
        result = lifting_cost(operating_costs, production)
        assert_decimal_equal(result, Decimal("50.00"))

    def test_lifting_cost_zero_production_raises_error(self):
        """Test that zero production raises error."""
        with pytest.raises(InvalidInputError):
            lifting_cost(Decimal("1000000"), Decimal("0"))


class TestNetback:
    """Test suite for netback function."""

    def test_netback_positive(self):
        """Test netback with profitable operations."""
        oil_price = Decimal("70.00")
        royalty = Decimal("10.00")
        operating_cost = Decimal("15.00")
        transport_cost = Decimal("5.00")
        result = netback(oil_price, royalty, operating_cost, transport_cost)
        assert_decimal_equal(result, Decimal("40.00"))

    def test_netback_high_costs(self):
        """Test netback with high costs reducing margin."""
        oil_price = Decimal("50.00")
        royalty = Decimal("8.00")
        operating_cost = Decimal("20.00")
        transport_cost = Decimal("7.00")
        result = netback(oil_price, royalty, operating_cost, transport_cost)
        assert_decimal_equal(result, Decimal("15.00"))

    def test_netback_negative(self):
        """Test netback can be negative when costs exceed price."""
        oil_price = Decimal("30.00")
        royalty = Decimal("5.00")
        operating_cost = Decimal("25.00")
        transport_cost = Decimal("10.00")
        result = netback(oil_price, royalty, operating_cost, transport_cost)
        assert_decimal_equal(result, Decimal("-10.00"))

    def test_netback_with_zero_price(self):
        """Test netback with zero oil price (edge case)."""
        oil_price = Decimal("0.00")
        royalty = Decimal("0.00")
        operating_cost = Decimal("15.00")
        transport_cost = Decimal("5.00")
        result = netback(oil_price, royalty, operating_cost, transport_cost)
        assert_decimal_equal(result, Decimal("-20.00"))


class TestBreakevenPrice:
    """Test suite for breakeven_price function."""

    def test_breakeven_standard(self):
        """Test breakeven price with standard costs."""
        total_costs = Decimal("500000000")  # $500M total costs
        production = Decimal("10000000")  # 10M BOE
        result = breakeven_price(total_costs, production)
        assert_decimal_equal(result, Decimal("50.00"))  # $50/barrel

    def test_breakeven_high_costs(self):
        """Test breakeven with high costs."""
        total_costs = Decimal("800000000")
        production = Decimal("10000000")
        result = breakeven_price(total_costs, production)
        assert_decimal_equal(result, Decimal("80.00"))

    def test_breakeven_zero_production_raises_error(self):
        """Test that zero production raises error."""
        with pytest.raises(InvalidInputError):
            breakeven_price(Decimal("1000000"), Decimal("0"))

    def test_breakeven_negative_production_raises_error(self):
        """Test that negative production raises error."""
        with pytest.raises(InvalidInputError):
            breakeven_price(Decimal("1000000"), Decimal("-100000"))


class TestOperatingNetbackMargin:
    """Test suite for operating_netback_margin function."""

    def test_onm_standard(self):
        """Test operating netback margin with standard inputs."""
        netback_value = Decimal("40.00")
        oil_price = Decimal("70.00")
        result = operating_netback_margin(netback_value, oil_price)
        assert_decimal_equal(result, Decimal("57.14"))  # ~57.14%

    def test_onm_high_margin(self):
        """Test ONM with high profitability."""
        netback_value = Decimal("50.00")
        oil_price = Decimal("60.00")
        result = operating_netback_margin(netback_value, oil_price)
        assert_decimal_equal(result, Decimal("83.33"))

    def test_onm_low_margin(self):
        """Test ONM with low profitability."""
        netback_value = Decimal("10.00")
        oil_price = Decimal("50.00")
        result = operating_netback_margin(netback_value, oil_price)
        assert_decimal_equal(result, Decimal("20.00"))

    def test_onm_zero_price_raises_error(self):
        """Test that zero oil price raises error."""
        with pytest.raises(InvalidInputError):
            operating_netback_margin(Decimal("10"), Decimal("0"))


class TestCapitalEfficiency:
    """Test suite for capital_efficiency function."""

    def test_ce_standard(self):
        """Test capital efficiency with standard inputs."""
        production_added = Decimal("5000")  # 5K BOE/day added
        capex = Decimal("100000000")  # $100M
        result = capital_efficiency(production_added, capex)
        assert_decimal_equal(result, Decimal("0.00"))  # 0.00005 BOE per dollar rounds to 0.00

    def test_ce_high_efficiency(self):
        """Test CE with high efficiency."""
        production_added = Decimal("10000")  # 10K BOE/day
        capex = Decimal("50000000")  # $50M
        result = capital_efficiency(production_added, capex)
        assert_decimal_equal(result, Decimal("0.00"))  # 0.0002 BOE per dollar rounds to 0.00

    def test_ce_low_efficiency(self):
        """Test CE with low efficiency."""
        production_added = Decimal("1000")  # 1K BOE/day
        capex = Decimal("100000000")  # $100M
        result = capital_efficiency(production_added, capex)
        assert_decimal_equal(result, Decimal("0.00"))  # 0.00001 BOE per dollar rounds to 0.00

    def test_ce_zero_capex_raises_error(self):
        """Test that zero capex raises error."""
        with pytest.raises(InvalidInputError):
            capital_efficiency(Decimal("1000000"), Decimal("0"))


class TestRecycleRatio:
    """Test suite for recycle_ratio function."""

    def test_recycle_ratio_profitable(self):
        """Test recycle ratio with profitable operations."""
        netback_value = Decimal("45.00")
        fd_cost = Decimal("15.00")
        result = recycle_ratio(netback_value, fd_cost)
        assert_decimal_equal(result, Decimal("3.00"))

    def test_recycle_ratio_marginal(self):
        """Test recycle ratio at marginal profitability."""
        netback_value = Decimal("20.00")
        fd_cost = Decimal("18.00")
        result = recycle_ratio(netback_value, fd_cost)
        assert_decimal_equal(result, Decimal("1.11"))

    def test_recycle_ratio_unprofitable(self):
        """Test recycle ratio with unprofitable operations."""
        netback_value = Decimal("10.00")
        fd_cost = Decimal("25.00")
        result = recycle_ratio(netback_value, fd_cost)
        assert_decimal_equal(result, Decimal("0.40"))

    def test_recycle_ratio_zero_fd_cost_raises_error(self):
        """Test that zero F&D cost raises error."""
        with pytest.raises(InvalidInputError):
            recycle_ratio(Decimal("30"), Decimal("0"))

    def test_recycle_ratio_negative_fd_cost_raises_error(self):
        """Test that negative F&D cost raises error."""
        with pytest.raises(InvalidInputError):
            recycle_ratio(Decimal("30"), Decimal("-15"))
