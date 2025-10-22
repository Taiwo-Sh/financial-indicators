[![Test](https://github.com/Taiwo-Sh/feconomics/actions/workflows/test.yaml/badge.svg)](https://github.com/Taiwo-Sh/feconomics/actions/workflows/test.yaml)
[![Code Quality](https://github.com/Taiwo-Sh/feconomics/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/Taiwo-Sh/feconomics/actions/workflows/code-quality.yaml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# feconomics

A comprehensive Python library for calculating essential financial and economic metrics with precision and ease. Built for financial analysts, investment professionals, and anyone working with financial data who needs accurate, reliable calculations.

## Why Financial Indicators?

When you're analyzing investments, evaluating companies, or making financial decisions, you need calculations you can trust. **Financial Indicators** provides:

- ✅ **Precision-first approach** using Python's Decimal type for accurate financial calculations
- ✅ **Clean, readable API** designed for both beginners and experts
- ✅ **Well-documented functions** with formulas, examples, and academic references
- ✅ **Industry-standard metrics** following CFA Institute and GAAP guidelines

## What Can You Calculate?

Financial Indicators covers seven core areas of financial analysis:

### 📈 Time Value of Money

Calculate the present and future value of cash flows, evaluate investment opportunities, and determine break-even points.

**Functions:** `net_present_value`, `internal_rate_of_return`, `present_value`, `future_value`, `annuity_present_value`, `annuity_future_value`, `payback_period`, `discounted_payback_period`

### 💰 Profitability Metrics

Measure how efficiently a company generates profit from its resources.

**Functions:** `return_on_investment`, `return_on_assets`, `return_on_equity`, `dupont_roe`, `gross_profit_margin`, `operating_profit_margin`, `net_profit_margin`, `ebitda`, `ebit`, `profitability_index`, `economic_value_added`

### 📊 Growth Analysis

Analyze revenue trends, earnings growth, and long-term sustainability.

**Functions:** `revenue_growth_rate`, `earnings_growth_rate`, `compound_annual_growth_rate`, `sustainable_growth_rate`, `retention_ratio`

### ⚠️ Risk Metrics

Quantify investment risk and volatility using industry-standard measures.

**Functions:** `beta`, `standard_deviation`, `variance`, `sharpe_ratio`, `sortino_ratio`, `value_at_risk_historical`, `conditional_var`, `maximum_drawdown`

### 💵 Cash Flow Analysis

Understand a company's cash generation and financial health.

**Functions:** `free_cash_flow`, `operating_cash_flow`, `unlevered_free_cash_flow`, `free_cash_flow_to_equity`, `free_cash_flow_to_firm`, `cash_flow_to_sales`, `cash_return_on_assets`, `cash_flow_margin`

### 🏦 Banking Metrics

Specialized ratios for analyzing banks and financial institutions.

**Functions:** `net_interest_margin`, `net_interest_income`, `efficiency_ratio`, `non_performing_loan_ratio`, `loan_loss_provision_ratio`, `coverage_ratio`, `capital_adequacy_ratio`, `tier1_capital_ratio`, `loan_to_deposit_ratio`

### 📉 Depreciation Methods

Calculate asset depreciation using various accounting methods including IRS-approved MACRS.

**Functions:** `straight_line_annual`, `straight_line_schedule`, `declining_balance_annual`, `declining_balance_schedule`, `sum_of_years_digits_annual`, `sum_of_years_digits_schedule`, `units_of_production_per_unit`, `units_of_production_period`, `units_of_production_schedule`, `macrs_annual`, `macrs_schedule`, `composite_rate`, `composite_life`, `composite_schedule`, `compare_methods`, `depreciation_tax_shield`, `book_value_at_year`

## Installation

Install using pip:

```bash
pip install feconomics
```

Or if you're using a modern Python package manager like `uv`:

```bash
uv add feconomics
```

### Requirements

- Python 3.8 or higher
- pandas >= 2.0.0 (for depreciation schedules)
- numpy >= 1.24.0

## Quick Start

Here's how easy it is to get started:

```python
from decimal import Decimal
from feconomics.core import time_value, profitability, growth

# Calculate NPV of an investment
cash_flows = [
    Decimal("-100000"),  # Initial investment
    Decimal("30000"),    # Year 1
    Decimal("40000"),    # Year 2
    Decimal("50000"),    # Year 3
]
npv = time_value.net_present_value(
    cash_flows=cash_flows,
    discount_rate=Decimal("0.1")
)
print(f"NPV: ${npv:,.2f}")  # NPV: $-1,192.12

# Calculate ROI for a profitable investment
roi = profitability.return_on_investment(
    net_profit=Decimal("15000"),
    total_investment=Decimal("50000")
)
print(f"ROI: {roi}%")  # ROI: 30.00%

# Calculate compound annual growth rate
cagr = growth.compound_annual_growth_rate(
    beginning_value=Decimal("10000"),
    ending_value=Decimal("16105.10"),
    periods=5
)
print(f"CAGR: {cagr * 100:.2f}%")  # CAGR: 10.00%
```

## Real-World Examples

### Example 1: Evaluating a Real Estate Investment

```python
from decimal import Decimal
from feconomics.core import time_value, profitability

# Property details
purchase_price = Decimal("500000")
down_payment = Decimal("100000")
annual_rental_income = Decimal("36000")
annual_expenses = Decimal("12000")
years_to_hold = 5
expected_sale_price = Decimal("600000")

# Calculate cash flows
net_annual_income = annual_rental_income - annual_expenses
cash_flows = [down_payment * -1]  # Initial investment

for year in range(years_to_hold):
    cash_flows.append(net_annual_income)

# Add sale proceeds in final year
cash_flows[-1] += expected_sale_price

# Calculate IRR
irr = time_value.internal_rate_of_return(cash_flows=cash_flows)
print(f"Expected IRR: {irr * 100:.2f}%")

# Calculate total ROI
total_profit = (expected_sale_price - purchase_price) + (net_annual_income * years_to_hold)
roi = profitability.return_on_investment(
    net_profit=total_profit,
    total_investment=down_payment
)
print(f"Total ROI: {roi:.2f}%")
```

### Example 2: Analyzing Company Performance

```python
from decimal import Decimal
from feconomics.core import profitability, growth, cash_flow

# Company financials (in millions)
revenue = Decimal("500")
cogs = Decimal("300")
operating_expenses = Decimal("100")
net_income = Decimal("60")
total_assets = Decimal("800")
shareholders_equity = Decimal("400")

# Previous year revenue
revenue_previous = Decimal("450")

# Profitability analysis
gross_margin = profitability.gross_profit_margin(
    gross_profit=revenue - cogs,
    revenue=revenue
)
net_margin = profitability.net_profit_margin(
    net_income=net_income,
    revenue=revenue
)
roa = profitability.return_on_assets(
    net_income=net_income,
    total_assets=total_assets
)
roe = profitability.return_on_equity(
    net_income=net_income,
    shareholders_equity=shareholders_equity
)

# Growth analysis
revenue_growth = growth.revenue_growth_rate(
    revenue_current=revenue,
    revenue_previous=revenue_previous
)

print(f"Gross Margin: {gross_margin:.2f}%")
print(f"Net Margin: {net_margin:.2f}%")
print(f"ROA: {roa:.2f}%")
print(f"ROE: {roe:.2f}%")
print(f"Revenue Growth: {revenue_growth * 100:.2f}%")
```

### Example 3: Risk Analysis of a Stock Portfolio

```python
from decimal import Decimal
from feconomics.core import risk

# Monthly returns for a stock (in decimal form)
stock_returns = [
    Decimal("0.05"), Decimal("-0.02"), Decimal("0.03"),
    Decimal("0.01"), Decimal("-0.04"), Decimal("0.06"),
    Decimal("0.02"), Decimal("-0.01"), Decimal("0.04"),
    Decimal("0.00"), Decimal("0.03"), Decimal("-0.02")
]

# Market returns for the same period
market_returns = [
    Decimal("0.03"), Decimal("-0.01"), Decimal("0.02"),
    Decimal("0.01"), Decimal("-0.02"), Decimal("0.04"),
    Decimal("0.02"), Decimal("0.00"), Decimal("0.03"),
    Decimal("0.01"), Decimal("0.02"), Decimal("-0.01")
]

# Calculate risk metrics
stock_volatility = risk.standard_deviation(returns=stock_returns)
stock_beta = risk.beta(
    asset_returns=stock_returns,
    market_returns=market_returns
)

# Calculate Sharpe ratio (assuming 2% risk-free rate annually, ~0.167% monthly)
risk_free_rate = Decimal("0.00167")
avg_return = sum(stock_returns) / len(stock_returns)
sharpe = risk.sharpe_ratio(
    portfolio_return=avg_return,
    risk_free_rate=risk_free_rate,
    standard_deviation=stock_volatility
)

# Calculate Value at Risk (95% confidence)
var_95 = risk.value_at_risk_historical(
    returns=stock_returns,
    confidence_level=Decimal("0.95")
)

print(f"Stock Volatility: {stock_volatility * 100:.2f}%")
print(f"Beta: {stock_beta:.2f}")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"VaR (95%): {var_95 * 100:.2f}%")
```

### Example 4: Depreciation Schedules for Tax Planning

```python
from decimal import Decimal
from feconomics.core import depreciation

# Equipment purchase
equipment_cost = Decimal("50000")
salvage_value = Decimal("5000")
useful_life = 5

# Compare depreciation methods
comparison = depreciation.compare_methods(
    cost=equipment_cost,
    salvage_value=salvage_value,
    useful_life=useful_life
)
print(comparison)

# Calculate MACRS depreciation for tax purposes (5-year property)
macrs_schedule = depreciation.macrs_schedule(
    cost=equipment_cost,
    recovery_period=5
)
print("\nMACRS Depreciation Schedule:")
print(macrs_schedule)

# Calculate tax shield from depreciation
tax_rate = Decimal("0.25")
year_1_depreciation = depreciation.macrs_annual(
    cost=equipment_cost,
    recovery_period=5,
    year=1
)
tax_shield = depreciation.depreciation_tax_shield(
    depreciation_expense=year_1_depreciation,
    tax_rate=tax_rate
)
print(f"\nYear 1 Tax Shield: ${tax_shield:,.2f}")
```

## Why Use Decimal Instead of Float?

Financial calculations require precision. Using Python's built-in `float` can lead to rounding errors:

```python
# ❌ Don't do this - float arithmetic can be imprecise
price = 0.1 + 0.2
print(price)  # 0.30000000000000004

# ✅ Do this instead - Decimal is precise
from decimal import Decimal
price = Decimal("0.1") + Decimal("0.2")
print(price)  # 0.3
```

All functions in this library use `Decimal` for accuracy. There's also a handy converter:

```python
from feconomics import d

# Convert numbers to Decimal easily
value = d(100.50)  # Decimal('100.50')
rate = d("0.05")   # Decimal('0.05')
```

## Advanced Features

### Banking Industry Metrics

Specialized functions for analyzing financial institutions:

```python
from decimal import Decimal
from feconomics.core import banking

# Calculate Net Interest Margin
nim = banking.net_interest_margin(
    net_interest_income=Decimal("500000"),
    average_earning_assets=Decimal("10000000")
)
print(f"NIM: {nim:.2f}%")  # Measures lending profitability

# Calculate Capital Adequacy Ratio (Basel III)
car = banking.capital_adequacy_ratio(
    tier1_capital=Decimal("1000000"),
    tier2_capital=Decimal("500000"),
    risk_weighted_assets=Decimal("10000000")
)
print(f"CAR: {car:.2f}%")  # Should be >= 8% per Basel requirements

# Check loan portfolio health
npl_ratio = banking.non_performing_loan_ratio(
    non_performing_loans=Decimal("150000"),
    total_loans=Decimal("5000000")
)
print(f"NPL Ratio: {npl_ratio:.2f}%")  # Lower is better
```

### Composite Depreciation for Asset Groups

Manage depreciation for multiple assets:

```python
from decimal import Decimal
from feconomics.core import depreciation

# Multiple assets with different useful lives
assets_costs = [
    Decimal("10000"),  # Computer equipment
    Decimal("50000"),  # Vehicle
    Decimal("100000")  # Machinery
]
salvage_values = [
    Decimal("1000"),
    Decimal("5000"),
    Decimal("10000")
]
useful_lives = [3, 5, 10]

# Calculate composite depreciation rate
comp_rate = depreciation.composite_rate(
    asset_costs=assets_costs,
    salvage_values=salvage_values,
    useful_lives=useful_lives
)

# Calculate composite life
comp_life = depreciation.composite_life(
    asset_costs=assets_costs,
    salvage_values=salvage_values,
    useful_lives=useful_lives
)

print(f"Composite Rate: {comp_rate * 100:.2f}%")
print(f"Composite Life: {comp_life:.2f} years")
```

## Error Handling

The library provides clear, actionable error messages:

```python
from decimal import Decimal
from feconomics.core import time_value
from feconomics.exceptions import InvalidInputError

try:
    # Empty cash flows
    npv = time_value.net_present_value(
        cash_flows=[],
        discount_rate=Decimal("0.1")
    )
except InvalidInputError as e:
    print(f"Error: {e}")  # "cash_flows cannot be empty"

try:
    # Negative discount rate
    npv = time_value.net_present_value(
        cash_flows=[Decimal("-1000"), Decimal("500")],
        discount_rate=Decimal("-0.1")
    )
except InvalidInputError as e:
    print(f"Error: {e}")  # "discount_rate must be non-negative"
```

## Testing and Quality

The library includes comprehensive tests and follows best practices for code quality.

Run tests yourself:

```bash
# Clone the repository
git clone https://github.com/Taiwo-Sh/feconomics.git
cd feconomics

# Install dependencies
pip install -e ".[test,dev]"

# Run tests
pytest

# Run with coverage report
pytest --cov=feconomics --cov-report=html
```

## Contributing

Contributions are welcome! Whether you want to:

- Add new financial metrics
- Improve documentation
- Report bugs
- Suggest features

Please feel free to open an issue or submit a pull request.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/Taiwo-Sh/feconomics.git
cd feconomics
pip install -e ".[test,dev]"

# Run linting
ruff check .

# Run type checking
mypy src/feconomics

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

This library implements financial formulas and metrics from:

- CFA Institute's curriculum on corporate finance and portfolio management
- Generally Accepted Accounting Principles (GAAP)
- International Financial Reporting Standards (IFRS)
- IRS Publication 946 (for MACRS depreciation)
- Academic textbooks including:
  - Brealey, Myers & Allen - "Principles of Corporate Finance"
  - Ross, Westerfield & Jordan - "Fundamentals of Corporate Finance"
  - Brigham & Ehrhardt - "Financial Management"

## Support

If you find this library helpful, please:

- ⭐ Star the repository on GitHub
- 📢 Share it with colleagues who might benefit
- 🐛 Report any issues you encounter
- 💡 Suggest improvements or new features

---

**Made with ❤️ for financial analysts, by financial analysts**
