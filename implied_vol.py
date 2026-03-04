"""
Implied volatility computation for a European call option.

This module computes the implied volatility by solving:

    Black-Scholes Call Price(sigma) = Market Price

The root-finding problem is solved using Brent's method
(scipy.optimize.brentq), a robust bracketing algorithm.

Why Brent instead of Newton-Raphson?
-------------------------------------
1. Brent is bracket-based:
   - It guarantees convergence if the function changes sign
     within the interval [a, b].
   - No need for a derivative.

2. Newton-Raphson:
   - Requires the derivative (Vega).
   - Can diverge if the initial guess is poor.
   - Can fail when Vega is very small (deep ITM/OTM or near expiry).
   - Sensitive to starting point.

3. Financial robustness:
   - Implied volatility inversion must be stable in production.
   - Brent is slower but far more reliable.
   - Reliability is preferred over speed in most pricing pipelines.

Brent combines:
- Bisection (guaranteed convergence)
- Secant method (faster convergence)
- Inverse quadratic interpolation (acceleration)

This makes it both robust and reasonably fast.
"""

from scipy.optimize import brentq
import numpy as np
from .model import call_price
def implied_vol_call(market_price, S, K, T, r):
    """
    Computes implied volatility for a European call option
    using Brent's method.

    Parameters
    ----------
    market_price : float
    S : float
    K : float
    T : float
    r : float

    Returns
    -------
    float or None
    """

    # No-arbitrage lower bound
    intrinsic = max(S - K * np.exp(-r * T), 0)

    # Basic arbitrage checks
    if market_price < intrinsic or market_price > S:
        return None

    def objective(sigma):
        return call_price(S, K, T, r, sigma) - market_price

    try:
        return brentq(objective, 1e-4, 3.0, maxiter=100)
    except ValueError:
        return None