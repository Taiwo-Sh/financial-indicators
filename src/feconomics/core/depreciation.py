"""Depreciation methods for asset accounting and financial analysis.

This module implements all standard depreciation methods including:
- Straight-Line
- Declining Balance (including Double Declining Balance)
- Sum-of-Years-Digits
- Units of Production
- MACRS (Modified Accelerated Cost Recovery System)
- Composite/Group Depreciation
"""

from decimal import Decimal
import typing

import pandas as pd

from feconomics.exceptions import InvalidInputError
from feconomics.validation import validate_non_negative, validate_positive

# MACRS Percentage Tables (IRS Publication 946)
MACRS_TABLES = {
    3: [Decimal("33.33"), Decimal("44.45"), Decimal("14.81"), Decimal("7.41")],
    5: [
        Decimal("20.00"),
        Decimal("32.00"),
        Decimal("19.20"),
        Decimal("11.52"),
        Decimal("11.52"),
        Decimal("5.76"),
    ],
    7: [
        Decimal("14.29"),
        Decimal("24.49"),
        Decimal("17.49"),
        Decimal("12.49"),
        Decimal("8.93"),
        Decimal("8.92"),
        Decimal("8.93"),
        Decimal("4.46"),
    ],
    10: [
        Decimal("10.00"),
        Decimal("18.00"),
        Decimal("14.40"),
        Decimal("11.52"),
        Decimal("9.22"),
        Decimal("7.37"),
        Decimal("6.55"),
        Decimal("6.55"),
        Decimal("6.56"),
        Decimal("6.55"),
        Decimal("3.28"),
    ],
    15: [
        Decimal("5.00"),
        Decimal("9.50"),
        Decimal("8.55"),
        Decimal("7.70"),
        Decimal("6.93"),
        Decimal("6.23"),
        Decimal("5.90"),
        Decimal("5.90"),
        Decimal("5.91"),
        Decimal("5.90"),
        Decimal("5.91"),
        Decimal("5.90"),
        Decimal("5.91"),
        Decimal("5.90"),
        Decimal("5.91"),
        Decimal("2.95"),
    ],
    20: [
        Decimal("3.750"),
        Decimal("7.219"),
        Decimal("6.677"),
        Decimal("6.177"),
        Decimal("5.713"),
        Decimal("5.285"),
        Decimal("4.888"),
        Decimal("4.522"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("4.462"),
        Decimal("4.461"),
        Decimal("2.231"),
    ],
}


def validate_depreciation_inputs(cost: Decimal, salvage_value: Decimal, useful_life: int) -> None:
    """
    Validate common depreciation inputs.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Useful life in years
    :raises InvalidInputError: If any input is invalid
    """
    validate_positive(cost, "cost")
    validate_non_negative(salvage_value, "salvage_value")

    if salvage_value >= cost:
        raise InvalidInputError(f"salvage_value ({salvage_value}) must be less than cost ({cost})")

    if useful_life <= 0:
        raise InvalidInputError(f"useful_life must be positive integer, got {useful_life}")


def straight_line_annual(cost: Decimal, salvage_value: Decimal, useful_life: int) -> Decimal:
    """
    Calculate annual straight-line depreciation.

    Formula:
        Annual Depreciation = (Cost - Salvage Value) / Useful Life

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value at end of useful life
    :param useful_life: Useful life in years (must be positive integer)
    :return: Annual depreciation expense
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        depreciation = straight_line_annual(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5
        )
        print(depreciation)  # Decimal('9000.00')
        ```

    References:
        - GAAP Accounting Standards Codification (ASC) 360
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)

    depreciable_base = cost - salvage_value
    annual_depreciation = depreciable_base / Decimal(useful_life)

    return annual_depreciation


def straight_line_schedule(cost: Decimal, salvage_value: Decimal, useful_life: int) -> pd.DataFrame:
    """
    Generate complete straight-line depreciation schedule.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Useful life in years
    :return: DataFrame with columns: Year, Depreciation_Expense,
             Accumulated_Depreciation, Book_Value
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        schedule = straight_line_schedule(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5
        )
        print(schedule)
        #    Year  Depreciation_Expense  Accumulated_Depreciation  Book_Value
        # 0     1                9000.0                   9000.0     41000.0
        # 1     2                9000.0                  18000.0     32000.0
        # 2     3                9000.0                  27000.0     23000.0
        # 3     4                9000.0                  36000.0     14000.0
        # 4     5                9000.0                  45000.0      5000.0
        ```
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)

    annual_depreciation = straight_line_annual(cost, salvage_value, useful_life)

    schedule = []
    accumulated = Decimal("0")

    for year in range(1, useful_life + 1):
        accumulated += annual_depreciation
        book_value = cost - accumulated

        schedule.append(
            {
                "Year": year,
                "Depreciation_Expense": float(annual_depreciation),
                "Accumulated_Depreciation": float(accumulated),
                "Book_Value": float(book_value),
            }
        )

    return pd.DataFrame(schedule)


def declining_balance_annual(
    book_value: Decimal, useful_life: int, factor: Decimal = Decimal("2.0")
) -> Decimal:
    """
    Calculate declining balance depreciation for current year.

    Formula:
        Depreciation Rate = Factor / Useful Life
        Depreciation = Book Value x Depreciation Rate

    :param book_value: Book value at beginning of year
    :param useful_life: Original useful life in years
    :param factor: Depreciation factor (1.5 or 2.0). Defaults to 2.0 (DDB)
    :return: Depreciation expense for the year
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        depreciation = declining_balance_annual(
            book_value=Decimal("50000"),
            useful_life=5,
            factor=Decimal("2.0")
        )
        print(depreciation)  # Decimal('20000.00') - 40% of $50,000
        ```
    """
    validate_positive(book_value, "book_value")
    if useful_life <= 0:
        raise InvalidInputError(f"useful_life must be positive integer, got {useful_life}")
    validate_positive(factor, "factor")

    rate = factor / Decimal(useful_life)
    depreciation = book_value * rate

    return depreciation


def declining_balance_schedule(
    cost: Decimal,
    salvage_value: Decimal,
    useful_life: int,
    factor: Decimal = Decimal("2.0"),
) -> pd.DataFrame:
    """
    Generate declining balance depreciation schedule.

    Formula:
        Rate = Factor / Useful Life
        Annual Depreciation = Book Value x Rate

    Note: Depreciation stops when book value reaches salvage value

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Useful life in years
    :param factor: Depreciation factor (default 2.0 for double declining)
    :return: DataFrame with depreciation schedule
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        # Double Declining Balance
        schedule = declining_balance_schedule(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5,
            factor=Decimal("2.0")
        )
        print(schedule)
        ```
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)
    validate_positive(factor, "factor")

    schedule = []
    book_value = cost
    accumulated = Decimal("0")
    rate = factor / Decimal(useful_life)

    for year in range(1, useful_life + 1):
        # Calculate depreciation but don't go below salvage value
        depreciation = book_value * rate

        # Ensure book value doesn't fall below salvage value
        if book_value - depreciation < salvage_value:
            depreciation = book_value - salvage_value

        accumulated += depreciation
        book_value -= depreciation

        schedule.append(
            {
                "Year": year,
                "Depreciation_Expense": float(depreciation),
                "Accumulated_Depreciation": float(accumulated),
                "Book_Value": float(book_value),
                "Depreciation_Rate": float(rate * 100),
            }
        )

        # Stop if we've reached salvage value
        if book_value <= salvage_value:
            break

    return pd.DataFrame(schedule)


def sum_of_years_digits_annual(
    cost: Decimal, salvage_value: Decimal, useful_life: int, year: int
) -> Decimal:
    """
    Calculate SYD depreciation for specific year.

    Formula:
        SYD = n(n+1)/2
        Year Depreciation = (Remaining Years / SYD) x Depreciable Base

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Total useful life in years
    :param year: Specific year to calculate (1 to useful_life)
    :return: Depreciation expense for specified year
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        year_1 = sum_of_years_digits_annual(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5,
            year=1
        )
        print(year_1)  # Decimal('15000.00') - highest depreciation
        ```
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)

    if not (1 <= year <= useful_life):
        raise InvalidInputError(f"year must be between 1 and {useful_life}, got {year}")

    # Calculate sum of years digits
    syd = Decimal(useful_life * (useful_life + 1)) / Decimal("2")

    # Remaining life for this year
    remaining_life = Decimal(useful_life - year + 1)

    # Depreciable base
    depreciable_base = cost - salvage_value

    # Calculate depreciation for this year
    depreciation = (remaining_life / syd) * depreciable_base

    return depreciation


def sum_of_years_digits_schedule(
    cost: Decimal, salvage_value: Decimal, useful_life: int
) -> pd.DataFrame:
    """
    Generate complete SYD depreciation schedule.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Useful life in years
    :return: DataFrame with depreciation schedule
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        schedule = sum_of_years_digits_schedule(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5
        )
        # Year 1 gets highest depreciation, decreasing each year
        print(schedule)
        ```
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)

    schedule = []
    accumulated = Decimal("0")
    syd = Decimal(useful_life * (useful_life + 1)) / Decimal("2")

    for year in range(1, useful_life + 1):
        depreciation = sum_of_years_digits_annual(cost, salvage_value, useful_life, year)
        accumulated += depreciation
        book_value = cost - accumulated

        remaining_life = useful_life - year + 1

        schedule.append(
            {
                "Year": year,
                "Remaining_Life": remaining_life,
                "SYD_Fraction": f"{remaining_life}/{int(syd)}",
                "Depreciation_Expense": float(depreciation),
                "Accumulated_Depreciation": float(accumulated),
                "Book_Value": float(book_value),
            }
        )

    return pd.DataFrame(schedule)


def units_of_production_per_unit(
    cost: Decimal, salvage_value: Decimal, total_units: Decimal
) -> Decimal:
    """
    Calculate depreciation per unit of production.

    Formula:
        Depreciation per Unit = (Cost - Salvage Value) / Total Expected Units

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param total_units: Total expected units over asset life
    :return: Depreciation expense per unit produced
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        per_unit = units_of_production_per_unit(
            cost=Decimal("100000"),
            salvage_value=Decimal("10000"),
            total_units=Decimal("500000")  # e.g., 500k units or miles
        )
        print(f"Depreciation per unit: ${per_unit}")  # $0.18 per unit
        ```
    """
    validate_positive(cost, "cost")
    validate_non_negative(salvage_value, "salvage_value")
    validate_positive(total_units, "total_units")

    if salvage_value >= cost:
        raise InvalidInputError(f"salvage_value ({salvage_value}) must be less than cost ({cost})")

    depreciable_base = cost - salvage_value
    per_unit_depreciation = depreciable_base / total_units

    return per_unit_depreciation


def units_of_production_period(
    cost: Decimal, salvage_value: Decimal, total_units: Decimal, units_produced: Decimal
) -> Decimal:
    """
    Calculate depreciation for a period based on units produced.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param total_units: Total expected units over asset life
    :param units_produced: Units produced in current period
    :return: Depreciation expense for the period
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal
        period_depreciation = units_of_production_period(
            cost=Decimal("100000"),
            salvage_value=Decimal("10000"),
            total_units=Decimal("500000"),
            units_produced=Decimal("50000")  # produced in this period
        )
        print(period_depreciation)  # Decimal('9000.00')
        ```
    """
    validate_non_negative(units_produced, "units_produced")

    per_unit = units_of_production_per_unit(cost, salvage_value, total_units)
    period_depreciation = per_unit * units_produced

    return period_depreciation


def units_of_production_schedule(
    cost: Decimal,
    salvage_value: Decimal,
    total_units: Decimal,
    units_per_period: typing.Sequence[Decimal],
) -> pd.DataFrame:
    """
    Generate units of production depreciation schedule.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param total_units: Total expected units over asset life
    :param units_per_period: List of units produced each period
    :return: DataFrame with depreciation schedule
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal

        # Machine expected to produce 500k units total
        # Actual production varies by year
        schedule = units_of_production_schedule(
            cost=Decimal("100000"),
            salvage_value=Decimal("10000"),
            total_units=Decimal("500000"),
            units_per_period=[
                Decimal("120000"),  # Year 1
                Decimal("150000"),  # Year 2
                Decimal("100000"),  # Year 3
                Decimal("80000"),   # Year 4
                Decimal("50000"),   # Year 5
            ]
        )
        print(schedule)
        ```
    """
    if not units_per_period:
        raise InvalidInputError("units_per_period cannot be empty")

    per_unit = units_of_production_per_unit(cost, salvage_value, total_units)

    schedule = []
    accumulated = Decimal("0")
    cumulative_units = Decimal("0")

    for period, units in enumerate(units_per_period, start=1):
        depreciation = per_unit * units
        accumulated += depreciation
        cumulative_units += units
        book_value = cost - accumulated

        schedule.append(
            {
                "Period": period,
                "Units_Produced": float(units),
                "Cumulative_Units": float(cumulative_units),
                "Per_Unit_Rate": float(per_unit),
                "Depreciation_Expense": float(depreciation),
                "Accumulated_Depreciation": float(accumulated),
                "Book_Value": float(book_value),
            }
        )

    return pd.DataFrame(schedule)


def macrs_annual(cost: Decimal, recovery_period: int, year: int) -> Decimal:
    """
    Calculate MACRS depreciation for specific year.

    MACRS uses IRS-provided percentage tables. No salvage value is used
    (assumed to be zero). Half-year convention applies in year 1.

    :param cost: Initial cost of asset (salvage value is not used in MACRS)
    :param recovery_period: MACRS recovery period (3, 5, 7, 10, 15, or 20 years)
    :param year: Specific year to calculate (1 to recovery_period+1)
    :return: Depreciation expense for specified year
    :raises InvalidInputError: If recovery_period is not a valid MACRS period

    Example:
        ```python
        from decimal import Decimal

        # 5-year property (e.g., computers, office equipment)
        year_1 = macrs_annual(Decimal("10000"), 5, 1)
        print(f"Year 1: ${year_1}")  # $2,000 (20% of $10,000)
        ```

    References:
        - IRS Publication 946: How to Depreciate Property
    """
    validate_positive(cost, "cost")

    if recovery_period not in MACRS_TABLES:
        valid_periods = ", ".join(str(p) for p in sorted(MACRS_TABLES.keys()))
        raise InvalidInputError(
            f"recovery_period must be one of {valid_periods}, got {recovery_period}"
        )

    table = MACRS_TABLES[recovery_period]

    if not (1 <= year <= len(table)):
        raise InvalidInputError(
            f"year must be between 1 and {len(table)} for "
            f"{recovery_period}-year property, got {year}"
        )

    percentage = table[year - 1]
    depreciation = cost * (percentage / 100)

    return depreciation


def macrs_schedule(cost: Decimal, recovery_period: int) -> pd.DataFrame:
    """
    Generate complete MACRS depreciation schedule.

    :param cost: Initial cost of asset
    :param recovery_period: MACRS recovery period (3, 5, 7, 10, 15, or 20)
    :return: DataFrame with MACRS depreciation schedule
    :raises InvalidInputError: If recovery_period is not valid

    Example:
        ```python
        from decimal import Decimal

        # 7-year property (e.g., office furniture, machinery)
        schedule = macrs_schedule(Decimal("50000"), 7)
        print(schedule)
        #    Year  MACRS_Rate  Depreciation  Accumulated  Book_Value
        # 0     1       14.29       7145.00      7145.00    42855.00
        # 1     2       24.49      12245.00     19390.00    30610.00
        # ...
        ```
    """
    validate_positive(cost, "cost")

    if recovery_period not in MACRS_TABLES:
        valid_periods = ", ".join(str(p) for p in sorted(MACRS_TABLES.keys()))
        raise InvalidInputError(
            f"recovery_period must be one of {valid_periods}, got {recovery_period}"
        )

    table = MACRS_TABLES[recovery_period]
    schedule = []
    accumulated = Decimal("0")

    for year, percentage in enumerate(table, start=1):
        depreciation = cost * (percentage / 100)
        accumulated += depreciation
        book_value = cost - accumulated

        schedule.append(
            {
                "Year": year,
                "MACRS_Rate": float(percentage),
                "Depreciation": float(depreciation),
                "Accumulated_Depreciation": float(accumulated),
                "Book_Value": float(book_value),
            }
        )

    return pd.DataFrame(schedule)


def composite_rate(
    asset_costs: typing.Sequence[Decimal],
    salvage_values: typing.Sequence[Decimal],
    useful_lives: typing.Sequence[int],
) -> Decimal:
    """
    Calculate composite depreciation rate for group of assets.

    Formula:
        Composite Rate = Σ(Annual Depreciation) / Σ(Asset Costs)

    :param asset_costs: List of individual asset costs
    :param salvage_values: List of salvage values (same order as costs)
    :param useful_lives: List of useful lives in years (same order as costs)
    :return: Composite depreciation rate as decimal
    :raises InvalidInputError: If lists have different lengths

    Example:
        ```python
        from decimal import Decimal

        rate = composite_rate(
            asset_costs=[Decimal("10000"), Decimal("20000"), Decimal("15000")],
            salvage_values=[Decimal("1000"), Decimal("2000"), Decimal("1500")],
            useful_lives=[5, 10, 8]
        )
        print(f"Composite Rate: {rate * 100}%")
        ```
    """
    if not (len(asset_costs) == len(salvage_values) == len(useful_lives)):
        raise InvalidInputError(
            "asset_costs, salvage_values, and useful_lives must have same length"
        )

    if not asset_costs:
        raise InvalidInputError("asset_costs cannot be empty")

    total_cost = Decimal("0")
    total_annual_depreciation = Decimal("0")

    for cost, salvage, life in zip(asset_costs, salvage_values, useful_lives):
        validate_depreciation_inputs(cost, salvage, life)
        total_cost += cost
        annual_dep = (cost - salvage) / Decimal(life)
        total_annual_depreciation += annual_dep

    composite_rate_value = total_annual_depreciation / total_cost
    return Decimal(composite_rate_value)


def composite_life(
    asset_costs: typing.Sequence[Decimal],
    salvage_values: typing.Sequence[Decimal],
    useful_lives: typing.Sequence[int],
) -> Decimal:
    """
    Calculate composite life for group of assets.

    Formula:
        Composite Life = Σ(Depreciable Base) / Σ(Annual Depreciation)

    :param asset_costs: List of individual asset costs
    :param salvage_values: List of salvage values
    :param useful_lives: List of useful lives in years
    :return: Composite life in years
    :raises InvalidInputError: If lists have different lengths

    Example:
        ```python
        from decimal import Decimal

        life = composite_life(
            asset_costs=[Decimal("10000"), Decimal("20000")],
            salvage_values=[Decimal("1000"), Decimal("2000")],
            useful_lives=[5, 10]
        )
        print(f"Composite Life: {life} years")
        ```
    """
    if not (len(asset_costs) == len(salvage_values) == len(useful_lives)):
        raise InvalidInputError(
            "asset_costs, salvage_values, and useful_lives must have same length"
        )

    if not asset_costs:
        raise InvalidInputError("asset_costs cannot be empty")

    total_depreciable_base = Decimal("0")
    total_annual_depreciation = Decimal("0")

    for cost, salvage, life in zip(asset_costs, salvage_values, useful_lives):
        validate_depreciation_inputs(cost, salvage, life)
        depreciable_base = cost - salvage
        total_depreciable_base += depreciable_base
        annual_dep = depreciable_base / Decimal(life)
        total_annual_depreciation += annual_dep

    composite_life_value = total_depreciable_base / total_annual_depreciation
    return Decimal(composite_life_value)


def composite_schedule(
    asset_costs: typing.Sequence[Decimal],
    salvage_values: typing.Sequence[Decimal],
    useful_lives: typing.Sequence[int],
    asset_names: typing.Sequence[str],
) -> pd.DataFrame:
    """
    Generate composite depreciation schedule for asset group.

    :param asset_costs: List of individual asset costs
    :param salvage_values: List of salvage values
    :param useful_lives: List of useful lives in years
    :param asset_names: List of asset names/descriptions
    :return: DataFrame with individual and composite depreciation
    :raises InvalidInputError: If lists have different lengths

    Example:
        ```python
        from decimal import Decimal

        schedule = composite_schedule(
            asset_costs=[Decimal("10000"), Decimal("20000")],
            salvage_values=[Decimal("1000"), Decimal("2000")],
            useful_lives=[5, 10],
            asset_names=["Equipment A", "Equipment B"]
        )
        print(schedule)
        ```
    """
    if not (len(asset_costs) == len(salvage_values) == len(useful_lives) == len(asset_names)):
        raise InvalidInputError("All input lists must have same length")

    if not asset_costs:
        raise InvalidInputError("asset_costs cannot be empty")

    # Calculate composite metrics
    comp_rate = composite_rate(asset_costs, salvage_values, useful_lives)
    comp_life = composite_life(asset_costs, salvage_values, useful_lives)

    schedule = []

    for name, cost, salvage, life in zip(asset_names, asset_costs, salvage_values, useful_lives):
        validate_depreciation_inputs(cost, salvage, life)

        depreciable_base = cost - salvage
        annual_depreciation = depreciable_base / Decimal(life)

        schedule.append(
            {
                "Asset_Name": name,
                "Cost": float(cost),
                "Salvage_Value": float(salvage),
                "Useful_Life": life,
                "Depreciable_Base": float(depreciable_base),
                "Annual_Depreciation": float(annual_depreciation),
            }
        )

    df = pd.DataFrame(schedule)

    # Add summary row
    totals = {
        "Asset_Name": "COMPOSITE TOTAL",
        "Cost": df["Cost"].sum(),
        "Salvage_Value": df["Salvage_Value"].sum(),
        "Useful_Life": float(comp_life),
        "Depreciable_Base": df["Depreciable_Base"].sum(),
        "Annual_Depreciation": df["Annual_Depreciation"].sum(),
    }

    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    df["Composite_Rate_%"] = float(comp_rate * 100)

    return df


def compare_methods(cost: Decimal, salvage_value: Decimal, useful_life: int) -> pd.DataFrame:
    """
    Compare different depreciation methods side-by-side.

    Generates a comparison table showing depreciation expense and book value
    for straight-line, declining balance, and SYD methods.

    :param cost: Initial cost of asset
    :param salvage_value: Estimated salvage value
    :param useful_life: Useful life in years
    :return: DataFrame comparing all methods
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal

        comparison = compare_methods(
            cost=Decimal("50000"),
            salvage_value=Decimal("5000"),
            useful_life=5
        )
        print(comparison)
        #    Year  SL_Depreciation  DDB_Depreciation  SYD_Depreciation
        # 0     1          9000.0           20000.0           15000.0
        # 1     2          9000.0           12000.0           12000.0
        # ...
        ```
    """
    validate_depreciation_inputs(cost, salvage_value, useful_life)

    # Generate schedules for each method
    sl_schedule = straight_line_schedule(cost, salvage_value, useful_life)
    ddb_schedule = declining_balance_schedule(cost, salvage_value, useful_life, Decimal("2.0"))
    syd_schedule = sum_of_years_digits_schedule(cost, salvage_value, useful_life)

    # Combine into comparison table
    comparison = pd.DataFrame(
        {
            "Year": sl_schedule["Year"],
            "SL_Depreciation": sl_schedule["Depreciation_Expense"],
            "SL_Book_Value": sl_schedule["Book_Value"],
            "DDB_Depreciation": ddb_schedule["Depreciation_Expense"],
            "DDB_Book_Value": ddb_schedule["Book_Value"],
            "SYD_Depreciation": syd_schedule["Depreciation_Expense"],
            "SYD_Book_Value": syd_schedule["Book_Value"],
        }
    )
    return comparison


def depreciation_tax_shield(depreciation_expense: Decimal, tax_rate: Decimal) -> Decimal:
    """
    Calculate tax shield value from depreciation.

    Formula:
        Tax Shield = Depreciation Expense x Tax Rate

    :param depreciation_expense: Annual depreciation expense
    :param tax_rate: Corporate tax rate as decimal (e.g., 0.21 for 21%)
    :return: Tax savings from depreciation
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal

        tax_shield = depreciation_tax_shield(
            depreciation_expense=Decimal("10000"),
            tax_rate=Decimal("0.21")
        )
        print(f"Tax Shield: ${tax_shield}")  # $2,100
        ```
    """
    validate_non_negative(depreciation_expense, "depreciation_expense")
    validate_non_negative(tax_rate, "tax_rate")

    if tax_rate > Decimal("1.0"):
        raise InvalidInputError(f"tax_rate should be decimal (e.g., 0.21 for 21%), got {tax_rate}")

    tax_shield = depreciation_expense * tax_rate

    return tax_shield


def book_value_at_year(cost: Decimal, accumulated_depreciation: Decimal) -> Decimal:
    """
    Calculate book value (carrying value) of asset.

    Formula:
        Book Value = Cost - Accumulated Depreciation

    :param cost: Original cost of asset
    :param accumulated_depreciation: Total depreciation taken to date
    :return: Current book value
    :raises InvalidInputError: If inputs are invalid

    Example:
        ```python
        from decimal import Decimal

        book_value = book_value_at_year(
            cost=Decimal("50000"),
            accumulated_depreciation=Decimal("18000")
        )
        print(f"Book Value: ${book_value}")  # $32,000
        ```
    """
    validate_positive(cost, "cost")
    validate_non_negative(accumulated_depreciation, "accumulated_depreciation")

    if accumulated_depreciation > cost:
        raise InvalidInputError(
            f"accumulated_depreciation ({accumulated_depreciation}) cannot exceed cost ({cost})"
        )

    book_value = cost - accumulated_depreciation
    return book_value
