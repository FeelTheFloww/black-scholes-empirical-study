# black_scholes/validation.py

import numpy as np
import pandas as pd
from .model import call_price, put_price, d1
from .implied_vol import implied_vol_call


def compute_mid_prices(df):
    df = df.copy()
    df["mid"] = (df["bid"] + df["ask"]) / 2
    return df


# ============================================================
# 1️⃣ IMPLIED VOL VALIDATION
# ============================================================

def compare_implied_vol(df, S, T, r):
    """
    Compare model-implied volatility with Yahoo implied volatility.

    Returns
    -------
    dict with:
        n_contracts
        mae
        max_error
        solver_failures
    """

    df = compute_mid_prices(df)

    errors = []
    failures = 0

    for _, row in df.iterrows():

        market_iv = row.get("impliedVolatility", None)
        market_price = row["mid"]
        K = row["strike"]

        if pd.isna(market_iv):
            continue

        model_iv = implied_vol_call(market_price, S, K, T, r)

        if model_iv is None:
            failures += 1
            continue

        errors.append(abs(model_iv - market_iv))

    if len(errors) == 0:
        return None

    return {
        "n_contracts": len(errors),
        "mae": np.mean(errors),
        "max_error": np.max(errors),
        "solver_failures": failures
    }


# ============================================================
# 2️⃣ PUT-CALL PARITY VALIDATION
# ============================================================

def put_call_parity_test(call_df, put_df, S, T, r, tolerance=1e-2):
    """
    Test put-call parity:

        C - P ?= S - K e^{-rT}

    Returns average absolute deviation.
    """

    call_df = compute_mid_prices(call_df)
    put_df = compute_mid_prices(put_df)

    merged = call_df.merge(
        put_df,
        on="strike",
        suffixes=("_call", "_put")
    )
    merged = merged[
    (merged["bid_call"] > 0) &
    (merged["ask_call"] > 0) &
    (merged["bid_put"] > 0) &
    (merged["ask_put"] > 0)
    ]
    merged = merged[
    (merged["mid_call"] > 0) &
    (merged["mid_put"] > 0)
]
    merged = merged[
    (merged["volume_call"] > 0) &
    (merged["volume_put"] > 0)
    ]
    merged = merged[
    abs(merged["strike"] - S) < 0.05 * S
    ]

    errors = []

    for _, row in merged.iterrows():

        C = row["mid_call"]
        P = row["mid_put"]
        K = row["strike"]

        rhs = S - K * np.exp(-r * T)
        lhs = C - P

        errors.append(abs(lhs - rhs))

    if len(errors) == 0:
        return None

    return {
        "n_pairs": len(errors),
        "mean_error": np.mean(errors),
        "max_error": np.max(errors)
    }


# ============================================================
# 3️⃣ NUMERICAL SANITY CHECKS
# ============================================================

def sanity_checks(S, K, T, r):

    results = {}

    # σ → 0
    discounted_intrinsic = max(S - K * np.exp(-r*T), 0)
    price_zero_vol = call_price(S, K, T, r, sigma=1e-8)
    results["zero_vol_check"] = abs(price_zero_vol - discounted_intrinsic)

    # T → 0
    intrinsic = max(S - K, 0)
    price_short_T = call_price(S, K, 1e-8, r, sigma=0.2)
    results["short_T_check"] = abs(price_short_T - intrinsic)

    return results