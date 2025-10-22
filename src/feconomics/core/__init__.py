"""
Core Financial Indicators Module.

This module provides essential financial analysis functions including:
- Time value of money calculations (NPV, IRR, PV, FV, payback period, etc.)
- Profitability metrics (ROI, ROE, ROA, margins, EBITDA, etc.)
- Growth metrics (revenue growth, CAGR, sustainable growth, etc.)
- Risk metrics (beta, Sharpe ratio, VaR, standard deviation, etc.)
- Cash flow analysis (FCF, FCFE, FCFF, OCF, etc.)
- Petroleum economics (F&D costs, netback, reserves, lifting costs, etc.)
- Banking metrics (NIM, NPL ratio, CAR, LTD ratio, etc.)
- Depreciation methods (straight-line, declining balance, SYD, MACRS, etc.)
"""

from . import banking  # noqa
from . import cash_flow  # noqa
from . import depreciation  # noqa
from . import growth  # noqa
from . import profitability  # noqa
from . import risk  # noqa
from . import time_value  # noqa
