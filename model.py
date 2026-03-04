"""

List of Parameters : 
----------
S : float
    Current price of the underlying asset
K : float
    Strike price
T : float
    Time to maturity (in years)
r : float
    Risk-free interest rate (annualized, continuous compounding)
sigma : float
    Volatility of the underlying asset (annualized)

Assumptions
-----------
- European options (no early exercise)
- No dividends
- Constant volatility and interest rate
- Log-normal asset price distribution
"""

import numpy as np
from scipy.stats import norm


def d1(S, K, T, r, sigma):
    """
    Compute the d1 term in the Black-Scholes formula.

    Returns
    -------
    float
        The d1 value used in option pricing formulas.
    """
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    """
    Compute the d2 term in the Black-Scholes formula.

    d2 = d1 - sigma * sqrt(T)

    Returns
    -------
    float
        The d2 value used in option pricing formulas.
    """
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def call_price(S, K, T, r, sigma):
    """
    Compute the price of a European call option using Black-Scholes formula.

    Returns
    -------
    float
        The theoretical price of the call option.
    """
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)


def put_price(S, K, T, r, sigma):
    """
    Compute the price of a European put option using Black-Scholes formula.

    Returns
    -------
    float
        The theoretical price of the put option.
    """
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)