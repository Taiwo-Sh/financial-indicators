"""Mathematical and financial constants for the financial_indicators package."""

from decimal import Decimal

# Common discount rates
DISCOUNT_RATE_LOW = Decimal("0.05")
DISCOUNT_RATE_MEDIUM = Decimal("0.10")
DISCOUNT_RATE_HIGH = Decimal("0.15")

# Days in year for financial calculations
DAYS_PER_YEAR = Decimal("365")
BUSINESS_DAYS_PER_YEAR = Decimal("252")

# Basis points
BASIS_POINT = Decimal("0.0001")

# Tolerance for iterative calculations
DEFAULT_TOLERANCE = Decimal("1e-6")
DEFAULT_MAX_ITERATIONS = 100

# Common conversion factors for oil & gas
BARRELS_PER_DAY_TO_ANNUAL = Decimal("365")
BBL_TO_BOE = 1  # Barrel of oil to barrel of oil equivalent
MCF_TO_BOE = Decimal("0.166667")  # Thousand cubic feet to BOE
