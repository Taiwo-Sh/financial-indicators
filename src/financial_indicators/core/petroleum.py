"""Petroleum economics metrics for oil and gas industry analysis."""

from decimal import Decimal

from financial_indicators.validation import validate_positive


def finding_development_cost(
    exploration_costs: Decimal, development_costs: Decimal, reserves_added: Decimal
) -> Decimal:
    """
    Calculate Finding & Development (F&D) Costs.

    F&D costs measure the cost per unit to find and develop new reserves,
    a key efficiency metric for oil and gas companies.

    Formula:
        F&D Cost = (Exploration Costs + Development Costs) / Reserves Added

    :param exploration_costs: Total exploration expenditures.
    :param development_costs: Total development expenditures.
    :param reserves_added: New reserves added (BOE - barrels of oil equivalent). Must be positive.
    :return: F&D cost in dollars per BOE.
    :raises InvalidInputError: If reserves_added is not positive.

    Example:
        ```python
        from decimal import Decimal
        exploration = Decimal("50000000")
        development = Decimal("150000000")
        reserves = Decimal("10000000")  # 10 million BOE
        fd_cost = finding_development_cost(exploration, development, reserves)
        print(fd_cost)  # Decimal('20.00') per BOE
        ```

    References:
        - Society of Petroleum Engineers (SPE). (2018). Petroleum Resources Management System.
        - Securities and Exchange Commission (SEC). Oil and Gas Reporting Requirements.
    """
    validate_positive(reserves_added, "reserves_added")

    fd_cost = (exploration_costs + development_costs) / reserves_added
    return fd_cost


def reserve_replacement_ratio(reserves_added: Decimal, production: Decimal) -> Decimal:
    """
    Calculate Reserve Replacement Ratio (RRR).

    RRR measures whether a company is replacing reserves faster than it's
    producing them, indicating long-term sustainability.

    Formula:
        RRR = Reserves Added / Production

    Interpretation:
        - RRR > 1.0: Reserves increasing (sustainable)
        - RRR = 1.0: Reserves flat (maintaining)
        - RRR < 1.0: Reserves declining (unsustainable)

    :param reserves_added: New reserves added (new discoveries + extensions + purchases) in BOE.
    :param production: Annual production volume in BOE. Must be positive.
    :return: Reserve replacement ratio.
    :raises InvalidInputError: If production is not positive.

    Example:
        ```python
        from decimal import Decimal
        reserves_added = Decimal("12000000")  # 12 million BOE
        annual_production = Decimal("10000000")  # 10 million BOE
        rrr = reserve_replacement_ratio(reserves_added, annual_production)
        print(rrr)  # Decimal('1.2000')
        ```

    References:
        - ExxonMobil. (2020). The Outlook for Energy.
        - BP Statistical Review of World Energy.
    """
    validate_positive(production, "production")

    rrr = reserves_added / production
    return rrr


def reserve_life_index(proved_reserves: Decimal, annual_production: Decimal) -> Decimal:
    """
    Calculate Reserve Life Index (RLI).

    RLI estimates how many years current reserves will last at
    current production rates.

    Formula:
        RLI = Proved Reserves / Annual Production

    :param proved_reserves: Total proved reserves in BOE. Must be positive.
    :param annual_production: Annual production rate in BOE. Must be positive.
    :return: Reserve life in years.
    :raises InvalidInputError: If proved_reserves or annual_production is not positive.

    Example:
        ```python
        from decimal import Decimal
        reserves = Decimal("100000000")  # 100 million BOE
        production = Decimal("10000000")  # 10 million BOE/year
        rli = reserve_life_index(reserves, production)
        print(rli)  # Decimal('10.00') years
        ```

    References:
        - Petroleum Resources Management System (PRMS). SPE/AAPG/WPC/SPEE.
    """
    validate_positive(proved_reserves, "proved_reserves")
    validate_positive(annual_production, "annual_production")

    rli = proved_reserves / annual_production
    return rli


def reserves_per_share(
    total_proved_reserves: Decimal, shares_outstanding: Decimal
) -> Decimal:
    """
    Calculate Reserves Per Share.

    This metric shows how many BOE of reserves exist for each share
    of stock, useful for valuation comparisons.

    Formula:
        Reserves per Share = Total Proved Reserves / Shares Outstanding

    :param total_proved_reserves: Total proved reserves in BOE. Must be positive.
    :param shares_outstanding: Number of shares outstanding. Must be positive.
    :return: Reserves per share in BOE.
    :raises InvalidInputError: If total_proved_reserves or shares_outstanding is not positive.

    Example:
        ```python
        from decimal import Decimal
        reserves = Decimal("100000000")  # 100 million BOE
        shares = Decimal("500000000")  # 500 million shares
        rps = reserves_per_share(reserves, shares)
        print(rps)  # Decimal('0.20') BOE per share
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
        - Energy sector analyst reports.
    """
    validate_positive(total_proved_reserves, "total_proved_reserves")
    validate_positive(shares_outstanding, "shares_outstanding")

    rps = total_proved_reserves / shares_outstanding
    return rps


def lifting_cost(total_operating_costs: Decimal, total_production: Decimal) -> Decimal:
    """
    Calculate Lifting Costs (Operating Costs per BOE).

    Lifting costs represent the operating expenses required to extract
    and bring hydrocarbons to the surface, per unit of production.

    Formula:
        Lifting Cost = Total Operating Costs / Total Production

    :param total_operating_costs: Total operating expenses in dollars.
    :param total_production: Total production volume in BOE. Must be positive.
    :return: Lifting cost in dollars per BOE.
    :raises InvalidInputError: If total_production is not positive.

    Example:
        ```python
        from decimal import Decimal
        opex = Decimal("50000000")
        production = Decimal("10000000")  # 10 million BOE
        lc = lifting_cost(opex, production)
        print(lc)  # Decimal('5.00') per BOE
        ```

    References:
        - Brock, H. et al. (2011). Petroleum Accounting.
        - Energy Information Administration (EIA). Cost of Production Reports.
    """
    validate_positive(total_production, "total_production")

    lc = total_operating_costs / total_production
    return lc


def netback(
    oil_price: Decimal,
    royalties: Decimal,
    transportation: Decimal,
    operating_costs: Decimal,
) -> Decimal:
    """
    Calculate Netback.

    Netback represents the net revenue per barrel after deducting
    all direct costs. It's a key profitability metric in oil and gas.

    Formula:
        Netback = Oil Price - Royalties - Transportation - Operating Costs

    :param oil_price: Realized oil price per barrel.
    :param royalties: Royalty payments per barrel.
    :param transportation: Transportation costs per barrel.
    :param operating_costs: Operating costs per barrel.
    :return: Netback in dollars per barrel.

    Example:
        ```python
        from decimal import Decimal
        price = Decimal("70.00")
        royalties = Decimal("10.00")
        transport = Decimal("5.00")
        opex = Decimal("15.00")
        nb = netback(price, royalties, transport, opex)
        print(nb)  # Decimal('40.00') per barrel
        ```

    References:
        - Canadian Association of Petroleum Producers (CAPP). Industry Statistics.
        - Wood Mackenzie. Upstream Cost Analysis.
    """
    nb = oil_price - royalties - transportation - operating_costs
    return nb


def breakeven_price(total_costs: Decimal, total_production: Decimal) -> Decimal:
    """
    Calculate Break-even Price.

    The break-even price is the minimum oil price needed to cover
    all costs (operating and capital).

    Formula:
        Break-even Price = Total Costs / Total Production

    :param total_costs: Total costs (operating + amortized capital costs).
    :param total_production: Total production volume in BOE. Must be positive.
    :return: Break-even price in dollars per BOE.
    :raises InvalidInputError: If total_production is not positive.

    Example:
        ```python
        from decimal import Decimal
        costs = Decimal("500000000")
        production = Decimal("10000000")  # 10 million BOE
        be = breakeven_price(costs, production)
        print(be)  # Decimal('50.00') per BOE
        ```

    References:
        - Rystad Energy. Break-even Analysis Reports.
        - IHS Markit. Upstream Economics.
    """
    validate_positive(total_production, "total_production")

    be = total_costs / total_production
    return be


def operating_netback_margin(netback: Decimal, oil_price: Decimal) -> Decimal:
    """
    Calculate Operating Netback Margin.

    This ratio shows what percentage of the oil price is retained
    as netback after costs.

    Formula:
        Operating Netback Margin = (Netback / Oil Price) x 100

    :param netback: Netback per barrel.
    :param oil_price: Oil price per barrel. Must be positive.
    :return: Operating netback margin as a percentage.
    :raises InvalidInputError: If oil_price is not positive.

    Example:
        ```python
        from decimal import Decimal
        netback = Decimal("35.00")
        price = Decimal("70.00")
        margin = operating_netback_margin(netback, price)
        print(margin)  # Decimal('50.00')
        ```

    References:
        - Canadian Natural Resources Limited. Financial Reports.
    """
    validate_positive(oil_price, "oil_price")

    margin = (netback / oil_price) * 100
    return margin


def capital_efficiency(
    production_added: Decimal, capital_expenditure: Decimal
) -> Decimal:
    """
    Calculate Capital Efficiency.

    Capital efficiency measures how much new production is achieved
    per dollar of capital invested.

    Formula:
        Capital Efficiency = Production Added / Capital Expenditure

    :param production_added: New production added (BOE/day or annual BOE). Must be positive.
    :param capital_expenditure: Total capital expenditure. Must be positive.
    :return: Capital efficiency (BOE per dollar).
    :raises InvalidInputError: If production_added or capital_expenditure is not positive.

    Example:
        ```python
        from decimal import Decimal
        production = Decimal("10000")  # BOE/day added
        capex = Decimal("500000000")
        ce = capital_efficiency(production, capex)
        print(ce)  # Decimal('0.00002') BOE/day per dollar
        ```

    References:
        - Morgan Stanley. E&P Capital Efficiency Analysis.
    """
    validate_positive(production_added, "production_added")
    validate_positive(capital_expenditure, "capital_expenditure")

    ce = production_added / capital_expenditure
    return ce


def recycle_ratio(
    operating_netback: Decimal, finding_development_cost: Decimal
) -> Decimal:
    """
    Calculate Recycle Ratio.

    Recycle ratio measures profitability by comparing netback to F&D costs.
    It shows how many times F&D costs are recovered from production.

    Formula:
        Recycle Ratio = Operating Netback / F&D Cost

    Interpretation:
        - Ratio > 2.0: Highly profitable
        - Ratio 1.0-2.0: Acceptable returns
        - Ratio < 1.0: Destroying value

    :param operating_netback: Operating netback per BOE.
    :param finding_development_cost: F&D cost per BOE. Must be positive.
    :return: Recycle ratio.
    :raises InvalidInputError: If finding_development_cost is not positive.

    Example:
        ```python
        from decimal import Decimal
        netback = Decimal("40.00")
        fd_cost = Decimal("15.00")
        ratio = recycle_ratio(netback, fd_cost)
        print(ratio)  # Decimal('2.6667')
        ```

    References:
        - Canadian oil and gas industry analysis.
        - PIW (Petroleum Intelligence Weekly). Recycle Ratio Rankings.
    """
    validate_positive(finding_development_cost, "finding_development_cost")

    ratio = operating_netback / finding_development_cost
    return ratio
