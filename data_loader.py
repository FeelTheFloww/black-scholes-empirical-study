"""
Option chain loader using yfinance.

This module retrieves available option expirations and
returns call option data for each expiration.

Notes
-----
- Some tickers (e.g. indices like ^GSPC) may not provide options.
- Network/API errors are not uncommon.
"""

import yfinance as yf


def load_option_chain(ticker_symbol: str) -> dict:
    """
    Load call option chains for all available expirations.

    Parameters
    ----------
    ticker_symbol : str
        Ticker symbol (e.g. "SPY", "AAPL").

    Returns
    -------
    dict
        Dictionary {expiration_date: DataFrame of call options}
    """

    ticker = yf.Ticker(ticker_symbol)

    try:
        expirations = ticker.options
    except Exception as e:
        raise RuntimeError(f"Failed to fetch options for {ticker_symbol}") from e

    if not expirations:
        return {}

    option_data = {}

    for exp in expirations:
        try:
            chain = ticker.option_chain(exp)
            option_data[exp] = chain.calls
        except Exception:
            # Skip expiration if API fails
            continue

    return option_data