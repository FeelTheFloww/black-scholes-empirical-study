## Project Motivation

This project started as an attempt to better understand how theoretical option pricing models relate to real market data.

Rather than implementing Black-Scholes only as a formula, the goal was to build a small quantitative pipeline able to:

- retrieve real option chains from the market
- compute implied volatility from observed prices
- verify theoretical relationships such as put-call parity
- visualize market phenomena such as the volatility smile

The project is designed as a first step toward a broader study of option pricing models.

---

## Design Decisions

Several implementation choices were made to prioritize robustness, numerical stability, and data reliability.

### 1. Real market data

Option chains are retrieved using `yfinance` to work with realistic market prices rather than synthetic data.

### 2. Mid-market pricing

Option prices are computed as:
mid = (bid + ask) / 2

Since the actual transaction price is not observable in the dataset, the midpoint between the bid and ask quotes is used as a proxy for the fair market price.

### 3. Robust implied volatility solver

Implied volatility is computed using **Brent’s method** instead of **Newton–Raphson**.

Brent's method:

- does not require derivatives
- guarantees convergence when the root is bracketed
- is more stable for deep ITM / OTM options

However, Newton–Raphson may be explored later to compare convergence speed and numerical stability.

### 4. Data filtering

Several filters are applied before computing implied volatility:

- positive bid/ask prices
- minimum open interest
- minimum trading volume
- limited bid-ask spread
- strikes close to the underlying price

These filters help remove illiquid options that could distort the analysis.

---

## Parameter Choices

Several parameters are fixed in the analysis. These choices are motivated by financial practice and data quality considerations.

### Risk-Free Rate (r)

The risk-free rate is set to:

r = 2%

This value is used as a simplified proxy for the short-term risk-free interest rate.

In practice, the risk-free rate should correspond to the yield of government bonds with maturity close to the option's time to expiration (for example US Treasury yields).

For the purpose of this study, a constant rate provides a reasonable approximation and simplifies the analysis.

---

### Time to Maturity (T)

The project focuses on options with maturities between roughly **30 and 90 days**.

The time to maturity is computed as:

T = (expiration_date - current_date) / 365.25


Short-dated options are preferred because:

- they are typically more liquid
- bid-ask spreads are smaller
- pricing discrepancies are easier to observe
- volatility smiles are often clearly visible

Restricting the maturity range helps maintain a more consistent dataset.

---

### Mid-Market Prices

The option price used in the analysis is defined as:


mid = (bid + ask) / 2


This is a standard approximation used in empirical option studies when transaction prices are unavailable.

Using the midpoint helps reduce the impact of the bid-ask spread.

---

### Strike Selection

To study the volatility smile, the analysis focuses on strikes around the current underlying price:


0.8 × S < K < 1.2 × S


This region typically contains the most liquid options and captures the main curvature of the implied volatility smile.

Deep in-the-money and deep out-of-the-money options are excluded because:

- they are often illiquid
- bid-ask spreads can be large
- implied volatility inversion becomes numerically unstable

---

### Liquidity Filters

Additional filters are applied to remove illiquid contracts:

- positive bid and ask prices
- minimum open interest
- minimum trading volume
- reasonable bid-ask spread

These filters improve the stability of implied volatility calculations.

---

### Implied Volatility Solver Range

The root search interval for implied volatility is set to:


0.0001 < σ < 3.0


This range covers realistic volatility levels observed in financial markets while avoiding numerical instability.

---

## Current Scope

The current version focuses on:

- Black-Scholes pricing
- implied volatility extraction
- volatility smile visualization
- validation of financial identities (put-call parity)

The goal is to build a reliable foundation before moving to more advanced models.

---

## Future Work

This project is intended to evolve.

Possible extensions include:

- volatility surface construction
- Greeks computation
- stochastic volatility models (Heston)
- smile parameterization (SVI / SABR)
- calibration of models to market data