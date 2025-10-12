"""Profitability metrics for financial analysis."""

from decimal import Decimal

from financial_indicators.validation import validate_non_zero, validate_positive


def return_on_investment(net_profit: Decimal, total_investment: Decimal) -> Decimal:
    """
    Calculate Return on Investment (ROI).

    ROI measures the gain or loss generated on an investment relative to
    the amount invested. It's one of the most widely used profitability ratios.

    Formula:
        ROI = (Net Profit / Total Investment) x 100

    :param net_profit: Net profit from investment (Total Returns - Total Costs).
    :param total_investment: Initial capital invested. Must be non-zero.
    :return: ROI as a percentage.
    :raises InvalidInputError: If total_investment is zero.

    Example:
        ```python
        from decimal import Decimal
        net_profit = Decimal("500")
        investment = Decimal("2000")
        roi = return_on_investment(net_profit, investment)
        print(roi)  # Decimal('25.00')
        ```

    References:
        - Brigham, E., & Ehrhardt, M. (2020). Financial Management.
    """
    validate_non_zero(total_investment, "total_investment")

    roi = (net_profit / total_investment) * 100
    return roi


def return_on_assets(net_income: Decimal, total_assets: Decimal) -> Decimal:
    """
    Calculate Return on Assets (ROA).

    ROA indicates how profitable a company is relative to its total assets.
    It shows how efficiently management uses assets to generate earnings.

    Formula:
        ROA = (Net Income / Total Assets) x 100

    :param net_income: Net profit after taxes.
    :param total_assets: Total value of assets. Must be positive.
    :return: ROA as a percentage.
    :raises InvalidInputError: If total_assets is not positive.

    Example:
        ```python
        from decimal import Decimal
        net_income = Decimal("50000")
        total_assets = Decimal("500000")
        roa = return_on_assets(net_income, total_assets)
        print(roa)  # Decimal('10.00')
        ```

    References:
        - Ross, S., Westerfield, R., & Jordan, B. (2019). Fundamentals of Corporate Finance.
    """
    validate_positive(total_assets, "total_assets")

    roa = (net_income / total_assets) * 100
    return roa


def return_on_equity(net_income: Decimal, shareholders_equity: Decimal) -> Decimal:
    """
    Calculate Return on Equity (ROE).

    ROE measures the profitability of a company in relation to shareholders' equity.
    It reveals how much profit a company generates with the money shareholders invested.

    Formula:
        ROE = (Net Income / Shareholders' Equity) x 100

    :param net_income: Net profit after taxes.
    :param shareholders_equity: Total shareholders' equity. Must be positive.
    :return: ROE as a percentage.
    :raises InvalidInputError: If shareholders_equity is not positive.

    Example:
        ```python
        from decimal import Decimal
        net_income = Decimal("50000")
        equity = Decimal("250000")
        roe = return_on_equity(net_income, equity)
        print(roe)  # Decimal('20.00')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    validate_positive(shareholders_equity, "shareholders_equity")

    roe = (net_income / shareholders_equity) * 100
    return roe


def dupont_roe(
    net_profit_margin: Decimal, asset_turnover: Decimal, equity_multiplier: Decimal
) -> Decimal:
    """
    Calculate Return on Equity using DuPont Analysis.

    DuPont Analysis breaks down ROE into three components to understand
    what drives profitability: operating efficiency, asset use efficiency,
    and financial leverage.

    Formula:
        ROE = Net Profit Margin x Asset Turnover x Equity Multiplier
            = (Net Income / Sales) x (Sales / Assets) x (Assets / Equity)

    :param net_profit_margin: Net profit margin as a ratio (not percentage).
    :param asset_turnover: Asset turnover ratio.
    :param equity_multiplier: Equity multiplier (leverage ratio).
    :return: ROE as a percentage.

    Example:
        ```python
        from decimal import Decimal
        npm = Decimal("0.10")  # 10% margin
        at = Decimal("1.5")    # 1.5x turnover
        em = Decimal("2.0")    # 2x leverage
        roe = dupont_roe(npm, at, em)
        print(roe)  # Decimal('30.00')
        ```

    References:
        - CFA Institute. (2021). Corporate Finance and Portfolio Management.
    """
    roe = net_profit_margin * asset_turnover * equity_multiplier * 100
    return roe


def gross_profit_margin(gross_profit: Decimal, revenue: Decimal) -> Decimal:
    """
    Calculate Gross Profit Margin.

    Gross profit margin shows the percentage of revenue that exceeds the cost
    of goods sold. It indicates pricing strategy and production efficiency.

    Formula:
        Gross Profit Margin = (Gross Profit / Revenue) x 100
        Where Gross Profit = Revenue - Cost of Goods Sold (COGS)

    :param gross_profit: Revenue minus COGS.
    :param revenue: Total revenue. Must be positive.
    :return: Gross profit margin as a percentage.
    :raises InvalidInputError: If revenue is not positive.

    Example:
        ```python
        from decimal import Decimal
        gross_profit = Decimal("400000")
        revenue = Decimal("1000000")
        gpm = gross_profit_margin(gross_profit, revenue)
        print(gpm)  # Decimal('40.00')
        ```

    References:
        - Brigham, E., & Houston, J. (2019). Fundamentals of Financial Management.
    """
    validate_positive(revenue, "revenue")

    margin = (gross_profit / revenue) * 100
    return margin


def operating_profit_margin(operating_income: Decimal, revenue: Decimal) -> Decimal:
    """
    Calculate Operating Profit Margin.

    Operating profit margin measures what proportion of revenue is left after
    paying for variable costs of production and operating expenses.

    Formula:
        Operating Profit Margin = (Operating Income / Revenue) x 100
        Where Operating Income = Gross Profit - Operating Expenses

    :param operating_income: Earnings before interest and taxes (EBIT).
    :param revenue: Total revenue. Must be positive.
    :return: Operating profit margin as a percentage.
    :raises InvalidInputError: If revenue is not positive.

    Example:
        ```python
        from decimal import Decimal
        operating_income = Decimal("200000")
        revenue = Decimal("1000000")
        opm = operating_profit_margin(operating_income, revenue)
        print(opm)  # Decimal('20.00')
        ```

    References:
        - Bodie, Z., Kane, A., & Marcus, A. (2018). Investments.
    """
    validate_positive(revenue, "revenue")

    margin = (operating_income / revenue) * 100
    return margin


def net_profit_margin(net_income: Decimal, revenue: Decimal) -> Decimal:
    """
    Calculate Net Profit Margin.

    Net profit margin shows what percentage of revenue remains as profit
    after all expenses, including taxes and interest, are paid.

    Formula:
        Net Profit Margin = (Net Income / Revenue) x 100

    :param net_income: Net profit after all expenses and taxes.
    :param revenue: Total revenue. Must be positive.
    :return: Net profit margin as a percentage.
    :raises InvalidInputError: If revenue is not positive.

    Example:
        ```python
        from decimal import Decimal
        net_income = Decimal("100000")
        revenue = Decimal("1000000")
        npm = net_profit_margin(net_income, revenue)
        print(npm)  # Decimal('10.00')
        ```

    References:
        - Brealey, R., Myers, S., & Allen, F. (2020). Principles of Corporate Finance.
    """
    validate_positive(revenue, "revenue")

    margin = (net_income / revenue) * 100
    return margin


def ebitda(
    net_income: Decimal,
    interest: Decimal,
    taxes: Decimal,
    depreciation: Decimal,
    amortization: Decimal,
) -> Decimal:
    """
    Calculate EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization).

    EBITDA is a measure of operating performance that excludes the effects of
    financing and accounting decisions.

    Formula:
        EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization

    :param net_income: Net profit after all expenses.
    :param interest: Interest expense.
    :param taxes: Tax expense.
    :param depreciation: Depreciation expense.
    :param amortization: Amortization expense.
    :return: EBITDA amount.

    Example:
        ```python
        from decimal import Decimal
        ni = Decimal("100000")
        interest = Decimal("20000")
        taxes = Decimal("30000")
        depreciation = Decimal("40000")
        amortization = Decimal("10000")
        result = ebitda(ni, interest, taxes, depreciation, amortization)
        print(result)  # Decimal('200000.00')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    result = net_income + interest + taxes + depreciation + amortization
    return result


def ebit(revenue: Decimal, cogs: Decimal, operating_expenses: Decimal) -> Decimal:
    """
    Calculate EBIT (Earnings Before Interest and Taxes).

    EBIT represents operating profit before the impact of financing decisions
    and tax environment.

    Formula:
        EBIT = Revenue - COGS - Operating Expenses

    :param revenue: Total revenue.
    :param cogs: Cost of goods sold.
    :param operating_expenses: Operating expenses (excluding depreciation/amortization).
    :return: EBIT amount.

    Example:
        ```python
        from decimal import Decimal
        revenue = Decimal("1000000")
        cogs = Decimal("600000")
        opex = Decimal("200000")
        result = ebit(revenue, cogs, opex)
        print(result)  # Decimal('200000.00')
        ```

    References:
        - Ross, S., Westerfield, R., & Jaffe, J. (2019). Corporate Finance.
    """
    result = revenue - cogs - operating_expenses
    return result


def profitability_index(
    present_value_cash_flows: Decimal, initial_investment: Decimal
) -> Decimal:
    """
    Calculate Profitability Index (PI).

    PI measures the ratio between the present value of future cash flows
    and the initial investment. It's used for capital budgeting decisions.

    Formula:
        PI = PV of Future Cash Flows / Initial Investment
        Or: PI = (NPV + Initial Investment) / Initial Investment

    Interpretation:
        - PI > 1.0: Project creates value (accept)
        - PI = 1.0: Project breaks even (indifferent)
        - PI < 1.0: Project destroys value (reject)

    :param present_value_cash_flows: Present value of all future cash flows.
    :param initial_investment: Initial investment amount. Must be positive.
    :return: Profitability index as a ratio.
    :raises InvalidInputError: If initial_investment is not positive.

    Example:
        ```python
        from decimal import Decimal
        pv_cash_flows = Decimal("1200000")
        investment = Decimal("1000000")
        pi = profitability_index(pv_cash_flows, investment)
        print(pi)  # Decimal('1.2000')
        ```

    References:
        - Berk, J., & DeMarzo, P. (2020). Corporate Finance.
    """
    validate_positive(initial_investment, "initial_investment")

    pi = present_value_cash_flows / initial_investment
    return pi


def economic_value_added(
    nopat: Decimal, capital_employed: Decimal, wacc: Decimal
) -> Decimal:
    """
    Calculate Economic Value Added (EVA).

    EVA measures the value created above the required return on capital.
    It represents true economic profit.

    Formula:
        EVA = NOPAT - (Capital Employed x WACC)

    :param nopat: Net Operating Profit After Tax.
    :param capital_employed: Total capital employed in the business. Must be positive.
    :param wacc: Weighted Average Cost of Capital as a decimal (e.g., 0.10 for 10%).
    :return: Economic value added in currency units.
    :raises InvalidInputError: If capital_employed is not positive.

    Example:
        ```python
        from decimal import Decimal
        nopat = Decimal("500000")
        capital = Decimal("2000000")
        wacc = Decimal("0.12")
        eva = economic_value_added(nopat, capital, wacc)
        print(eva)  # Decimal('260000.00')
        ```

    References:
        - Stewart, G.B. (1991). The Quest for Value. Harper Business.
    """
    validate_positive(capital_employed, "capital_employed")

    eva = nopat - (capital_employed * wacc)
    return eva
