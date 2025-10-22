"""Banking metrics for financial institution analysis."""

from decimal import Decimal

from feconomics.exceptions import InvalidInputError
from feconomics.validation import validate_non_negative, validate_positive


def net_interest_margin(net_interest_income: Decimal, average_earning_assets: Decimal) -> Decimal:
    """
    Calculate Net Interest Margin (NIM).

    Formula:
        NIM = (Net Interest Income / Average Earning Assets) x 100

    :param net_interest_income: Interest income minus interest expense.
    :param average_earning_assets: Average interest-earning assets. Must be positive.
    :return: NIM as a percentage.
    :raises InvalidInputError: If average_earning_assets is not positive.

    Example:
        ```python
        from decimal import Decimal
        nii = Decimal("50000000")
        assets = Decimal("1000000000")
        nim = net_interest_margin(nii, assets)
        print(nim)  # Decimal('5.00') - 5% NIM
        ```

    References:
        - Bank profitability analysis.
    """
    validate_positive(average_earning_assets, "average_earning_assets")

    nim = (net_interest_income / average_earning_assets) * 100
    return nim


def net_interest_income(interest_income: Decimal, interest_expense: Decimal) -> Decimal:
    """
    Calculate Net Interest Income (NII).

    Formula:
        NII = Interest Income - Interest Expense

    :param interest_income: Total interest income. Must be non-negative.
    :param interest_expense: Total interest expense. Must be non-negative.
    :return: Net interest income.
    :raises InvalidInputError: If inputs are negative.

    Example:
        ```python
        from decimal import Decimal
        income = Decimal("75000000")
        expense = Decimal("25000000")
        nii = net_interest_income(income, expense)
        print(nii)  # Decimal('50000000.00')
        ```

    References:
        - Banking income statement analysis.
    """
    validate_non_negative(interest_income, "interest_income")
    validate_non_negative(interest_expense, "interest_expense")

    nii = interest_income - interest_expense
    return nii


def efficiency_ratio(non_interest_expense: Decimal, revenue: Decimal) -> Decimal:
    """
    Calculate Efficiency Ratio.

    Formula:
        Efficiency Ratio = (Non-Interest Expense / Revenue) x 100

    Interpretation:
        - Ratio < 50%: Efficient
        - Ratio 50-60%: Average
        - Ratio > 60%: Inefficient

    :param non_interest_expense: Non-interest expenses. Must be non-negative.
    :param revenue: Total revenue (NII + non-interest income). Must be positive.
    :return: Efficiency ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        expense = Decimal("40000000")
        revenue = Decimal("80000000")
        efficiency = efficiency_ratio(expense, revenue)
        print(efficiency)  # Decimal('50.00') - 50%
        ```

    References:
        - Bank operating efficiency metrics.
    """
    validate_non_negative(non_interest_expense, "non_interest_expense")
    validate_positive(revenue, "revenue")

    ratio = (non_interest_expense / revenue) * 100
    return ratio


def non_performing_loan_ratio(non_performing_loans: Decimal, total_loans: Decimal) -> Decimal:
    """
    Calculate Non-Performing Loan (NPL) Ratio.

    Formula:
        NPL Ratio = (Non-Performing Loans / Total Loans) x 100

    Interpretation:
        - Ratio < 2%: Good asset quality
        - Ratio 2-5%: Acceptable
        - Ratio > 5%: Poor asset quality

    :param non_performing_loans: Loans past due or in default. Must be non-negative.
    :param total_loans: Total loan portfolio. Must be positive.
    :return: NPL ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        npl = Decimal("30000000")
        total = Decimal("1000000000")
        ratio = non_performing_loan_ratio(npl, total)
        print(ratio)  # Decimal('3.00') - 3% NPL
        ```

    References:
        - Basel Committee on Banking Supervision guidelines.
    """
    validate_non_negative(non_performing_loans, "non_performing_loans")
    validate_positive(total_loans, "total_loans")

    if non_performing_loans > total_loans:
        raise InvalidInputError("non_performing_loans cannot exceed total_loans")

    ratio = (non_performing_loans / total_loans) * 100
    return ratio


def loan_loss_provision_ratio(loan_loss_provision: Decimal, total_loans: Decimal) -> Decimal:
    """
    Calculate Loan Loss Provision Ratio.

    Formula:
        Provision Ratio = (Loan Loss Provision / Total Loans) x 100

    :param loan_loss_provision: Provision for loan losses. Must be non-negative.
    :param total_loans: Total loan portfolio. Must be positive.
    :return: Provision ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        provision = Decimal("15000000")
        total = Decimal("1000000000")
        ratio = loan_loss_provision_ratio(provision, total)
        print(ratio)  # Decimal('1.50') - 1.5%
        ```

    References:
        - Credit risk management metrics.
    """
    validate_non_negative(loan_loss_provision, "loan_loss_provision")
    validate_positive(total_loans, "total_loans")

    ratio = (loan_loss_provision / total_loans) * 100
    return ratio


def coverage_ratio(loan_loss_reserves: Decimal, non_performing_loans: Decimal) -> Decimal:
    """
    Calculate Coverage Ratio (Allowance for Loan Losses / NPLs).

    Formula:
        Coverage Ratio = (Loan Loss Reserves / Non-Performing Loans) x 100

    Interpretation:
        - Ratio > 100%: Adequate coverage
        - Ratio < 100%: Insufficient coverage

    :param loan_loss_reserves: Allowance for loan losses. Must be non-negative.
    :param non_performing_loans: Total non-performing loans. Must be positive.
    :return: Coverage ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        reserves = Decimal("40000000")
        npl = Decimal("30000000")
        ratio = coverage_ratio(reserves, npl)
        print(ratio)  # Decimal('133.33') - 133.33% coverage
        ```

    References:
        - Credit risk provisioning standards.
    """
    validate_non_negative(loan_loss_reserves, "loan_loss_reserves")
    validate_positive(non_performing_loans, "non_performing_loans")

    ratio = (loan_loss_reserves / non_performing_loans) * 100
    return ratio


def capital_adequacy_ratio(
    tier1_capital: Decimal, tier2_capital: Decimal, risk_weighted_assets: Decimal
) -> Decimal:
    """
    Calculate Capital Adequacy Ratio (CAR).

    Formula:
        CAR = ((Tier 1 Capital + Tier 2 Capital) / Risk-Weighted Assets) x 100

    Regulatory Minimum:
        - Basel III: 8% minimum

    :param tier1_capital: Tier 1 capital (core capital). Must be non-negative.
    :param tier2_capital: Tier 2 capital (supplementary capital). Must be non-negative.
    :param risk_weighted_assets: Risk-weighted assets. Must be positive.
    :return: CAR as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        tier1 = Decimal("120000000")
        tier2 = Decimal("30000000")
        rwa = Decimal("1000000000")
        car = capital_adequacy_ratio(tier1, tier2, rwa)
        print(car)  # Decimal('15.00') - 15% CAR
        ```

    References:
        - Basel III capital requirements.
    """
    validate_non_negative(tier1_capital, "tier1_capital")
    validate_non_negative(tier2_capital, "tier2_capital")
    validate_positive(risk_weighted_assets, "risk_weighted_assets")

    total_capital = tier1_capital + tier2_capital
    car = (total_capital / risk_weighted_assets) * 100
    return car


def tier1_capital_ratio(tier1_capital: Decimal, risk_weighted_assets: Decimal) -> Decimal:
    """
    Calculate Tier 1 Capital Ratio.

    Formula:
        Tier 1 Ratio = (Tier 1 Capital / Risk-Weighted Assets) x 100

    Regulatory Minimum:
        - Basel III: 6% minimum

    :param tier1_capital: Tier 1 capital. Must be non-negative.
    :param risk_weighted_assets: Risk-weighted assets. Must be positive.
    :return: Tier 1 ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        tier1 = Decimal("120000000")
        rwa = Decimal("1000000000")
        ratio = tier1_capital_ratio(tier1, rwa)
        print(ratio)  # Decimal('12.00') - 12%
        ```

    References:
        - Basel III Tier 1 requirements.
    """
    validate_non_negative(tier1_capital, "tier1_capital")
    validate_positive(risk_weighted_assets, "risk_weighted_assets")

    ratio = (tier1_capital / risk_weighted_assets) * 100
    return ratio


def loan_to_deposit_ratio(total_loans: Decimal, total_deposits: Decimal) -> Decimal:
    """
    Calculate Loan-to-Deposit (LTD) Ratio.

    Formula:
        LTD = (Total Loans / Total Deposits) x 100

    Interpretation:
        - Ratio < 80%: Conservative lending
        - Ratio 80-90%: Balanced
        - Ratio > 90%: Aggressive lending

    :param total_loans: Total loan portfolio. Must be non-negative.
    :param total_deposits: Total customer deposits. Must be positive.
    :return: LTD ratio as a percentage.
    :raises InvalidInputError: If inputs violate constraints.

    Example:
        ```python
        from decimal import Decimal
        loans = Decimal("800000000")
        deposits = Decimal("1000000000")
        ratio = loan_to_deposit_ratio(loans, deposits)
        print(ratio)  # Decimal('80.00') - 80%
        ```

    References:
        - Bank liquidity management metrics.
    """
    validate_non_negative(total_loans, "total_loans")
    validate_positive(total_deposits, "total_deposits")

    ratio = (total_loans / total_deposits) * 100
    return ratio
