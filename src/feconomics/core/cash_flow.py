"""Cash flow analysis metrics for financial analysis."""

from decimal import Decimal

from feconomics.validation import validate_positive


def free_cash_flow(operating_cash_flow: Decimal, capital_expenditures: Decimal) -> Decimal:
    """
    Calculate Free Cash Flow (FCF).

    FCF represents cash available after paying for operations and capital
    investments. It's a key measure of financial performance and valuation.

    Formula:
        FCF = Operating Cash Flow - Capital Expenditures

    :param operating_cash_flow: Cash generated from operations.
    :param capital_expenditures: Cash spent on fixed assets.
    :return: Free cash flow.

    Example:
        ```python
        from decimal import Decimal
        ocf = Decimal("500000")
        capex = Decimal("150000")
        fcf = free_cash_flow(ocf, capex)
        print(fcf)  # Decimal('350000.00')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    fcf = operating_cash_flow - capital_expenditures
    return fcf


def operating_cash_flow(
    net_income: Decimal,
    depreciation: Decimal,
    amortization: Decimal,
    change_in_working_capital: Decimal,
) -> Decimal:
    """
    Calculate Operating Cash Flow (OCF).

    OCF measures cash generated from normal business operations.

    Formula:
        OCF = Net Income + Depreciation + Amortization - Change in Working Capital

    :param net_income: Net income after taxes.
    :param depreciation: Depreciation expense.
    :param amortization: Amortization expense.
    :param change_in_working_capital: Increase in working capital (use negative for decrease).
    :return: Operating cash flow.

    Example:
        ```python
        from decimal import Decimal
        ni = Decimal("200000")
        depr = Decimal("50000")
        amort = Decimal("10000")
        wc_change = Decimal("20000")
        ocf = operating_cash_flow(ni, depr, amort, wc_change)
        print(ocf)  # Decimal('240000.00')
        ```

    References:
        - Ross, S., Westerfield, R., & Jordan, B. (2019). Fundamentals of Corporate Finance.
    """
    ocf = net_income + depreciation + amortization - change_in_working_capital
    return ocf


def unlevered_free_cash_flow(
    ebit: Decimal,
    tax_rate: Decimal,
    depreciation: Decimal,
    capex: Decimal,
    change_in_nwc: Decimal,
) -> Decimal:
    """
    Calculate Unlevered Free Cash Flow.

    Unlevered FCF represents cash flow available to all investors
    (debt and equity holders) before debt payments.

    Formula:
        Unlevered FCF = EBIT x (1 - Tax Rate) + Depreciation - CAPEX - Change in NWC

    :param ebit: Earnings before interest and taxes.
    :param tax_rate: Tax rate as decimal (e.g., 0.21 for 21%).
    :param depreciation: Depreciation expense.
    :param capex: Capital expenditures.
    :param change_in_nwc: Change in net working capital.
    :return: Unlevered free cash flow.

    Example:
        ```python
        from decimal import Decimal
        ebit = Decimal("500000")
        tax_rate = Decimal("0.21")
        depr = Decimal("50000")
        capex = Decimal("100000")
        nwc_change = Decimal("20000")
        ufcf = unlevered_free_cash_flow(ebit, tax_rate, depr, capex, nwc_change)
        print(ufcf)  # Decimal('325000.00')
        ```

    References:
        - Koller, T., Goedhart, M., & Wessels, D. (2020). Valuation.
    """
    nopat = ebit * (1 - tax_rate)
    ufcf = nopat + depreciation - capex - change_in_nwc
    return ufcf


def free_cash_flow_to_equity(
    net_income: Decimal,
    depreciation: Decimal,
    capex: Decimal,
    change_in_nwc: Decimal,
    net_borrowing: Decimal,
) -> Decimal:
    """
    Calculate Free Cash Flow to Equity (FCFE).

    FCFE represents cash flow available to equity holders after all
    expenses, reinvestment, and debt payments.

    Formula:
        FCFE = Net Income + Depreciation - CAPEX - Change in NWC + Net Borrowing

    :param net_income: Net income after taxes and interest.
    :param depreciation: Depreciation and amortization expense.
    :param capex: Capital expenditures.
    :param change_in_nwc: Change in net working capital.
    :param net_borrowing: New debt issued minus debt repayments.
    :return: Free cash flow to equity.

    Example:
        ```python
        from decimal import Decimal
        ni = Decimal("200000")
        depr = Decimal("50000")
        capex = Decimal("100000")
        nwc_change = Decimal("20000")
        borrowing = Decimal("30000")
        fcfe = free_cash_flow_to_equity(ni, depr, capex, nwc_change, borrowing)
        print(fcfe)  # Decimal('160000.00')
        ```

    References:
        - Damodaran, A. (2012). Investment Valuation.
    """
    fcfe = net_income + depreciation - capex - change_in_nwc + net_borrowing
    return fcfe


def free_cash_flow_to_firm(
    ebit: Decimal,
    tax_rate: Decimal,
    depreciation: Decimal,
    capex: Decimal,
    change_in_nwc: Decimal,
) -> Decimal:
    """
    Calculate Free Cash Flow to Firm (FCFF).

    FCFF represents cash flow available to all investors (both debt
    and equity holders) after investments.

    Formula:
        FCFF = EBIT x (1 - Tax Rate) + Depreciation - CAPEX - Change in NWC

    :param ebit: Earnings before interest and taxes.
    :param tax_rate: Tax rate as decimal (e.g., 0.21 for 21%).
    :param depreciation: Depreciation and amortization expense.
    :param capex: Capital expenditures.
    :param change_in_nwc: Change in net working capital.
    :return: Free cash flow to firm.

    Example:
        ```python
        from decimal import Decimal
        ebit = Decimal("500000")
        tax_rate = Decimal("0.21")
        depr = Decimal("50000")
        capex = Decimal("100000")
        nwc_change = Decimal("20000")
        fcff = free_cash_flow_to_firm(ebit, tax_rate, depr, capex, nwc_change)
        print(fcff)  # Decimal('325000.00')
        ```

    References:
        - CFA Institute. (2021). Corporate Finance and Portfolio Management.
    """
    nopat = ebit * (1 - tax_rate)
    fcff = nopat + depreciation - capex - change_in_nwc
    return fcff


def cash_flow_to_sales(operating_cash_flow: Decimal, net_sales: Decimal) -> Decimal:
    """
    Calculate Cash Flow to Sales Ratio.

    This ratio shows how much cash is generated per dollar of sales,
    indicating operational efficiency.

    Formula:
        Cash Flow to Sales = Operating Cash Flow / Net Sales

    :param operating_cash_flow: Cash from operating activities.
    :param net_sales: Total net sales. Must be positive.
    :return: Cash flow to sales ratio.
    :raises InvalidInputError: If net_sales is not positive.

    Example:
        ```python
        from decimal import Decimal
        ocf = Decimal("300000")
        sales = Decimal("2000000")
        ratio = cash_flow_to_sales(ocf, sales)
        print(ratio)  # Decimal('0.1500')
        ```

    References:
        - Brigham, E., & Ehrhardt, M. (2020). Financial Management.
    """
    validate_positive(net_sales, "net_sales")

    ratio = operating_cash_flow / net_sales
    return ratio


def cash_return_on_assets(operating_cash_flow: Decimal, total_assets: Decimal) -> Decimal:
    """
    Calculate Cash Return on Assets.

    This metric shows how efficiently a company generates cash from its assets.

    Formula:
        Cash Return on Assets = Operating Cash Flow / Total Assets

    :param operating_cash_flow: Cash from operating activities.
    :param total_assets: Total assets. Must be positive.
    :return: Cash return on assets ratio.
    :raises InvalidInputError: If total_assets is not positive.

    Example:
        ```python
        from decimal import Decimal
        ocf = Decimal("300000")
        assets = Decimal("2000000")
        croa = cash_return_on_assets(ocf, assets)
        print(croa)  # Decimal('0.1500')
        ```

    References:
        - Bodie, Z., Kane, A., & Marcus, A. (2018). Investments.
    """
    validate_positive(total_assets, "total_assets")

    ratio = operating_cash_flow / total_assets
    return ratio


def cash_flow_margin(operating_cash_flow: Decimal, revenue: Decimal) -> Decimal:
    """
    Calculate Cash Flow Margin.

    Cash flow margin measures the percentage of revenue converted into
    operating cash flow.

    Formula:
        Cash Flow Margin = (Operating Cash Flow / Revenue) x 100

    :param operating_cash_flow: Cash from operating activities.
    :param revenue: Total revenue. Must be positive.
    :return: Cash flow margin as a percentage.
    :raises InvalidInputError: If revenue is not positive.

    Example:
        ```python
        from decimal import Decimal
        ocf = Decimal("300000")
        revenue = Decimal("2000000")
        cfm = cash_flow_margin(ocf, revenue)
        print(cfm)  # Decimal('15.00')
        ```

    References:
        - Brealey, R., Myers, S., & Allen, F. (2020). Principles of Corporate Finance.
    """
    validate_positive(revenue, "revenue")

    margin = (operating_cash_flow / revenue) * 100
    return margin
