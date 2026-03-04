# black_scholes/smile.py

import numpy as np
import matplotlib.pyplot as plt
from .implied_vol import implied_vol_call


def compute_smile(df, S, T, r):

    strikes = []
    vols = []

    df = df.copy()

    # Mid price
    df["mid"] = (df["bid"] + df["ask"]) / 2

    # Basic filters
    df = df[
    (df["bid"] > 0) &
    (df["ask"] > 0) &
    (df["openInterest"] > 50) &
    (df["volume"] > 10)
    ]

    df["mid"] = (df["bid"] + df["ask"]) / 2

    df = df[(df["ask"] - df["bid"]) / df["mid"] < 0.3]

    # Strike filter around ATM
    df = df[(df["strike"] > 0.8*S) & (df["strike"] < 1.2*S)]

    for _, row in df.iterrows():
        iv = implied_vol_call(row["mid"], S, row["strike"], T, r)

        if iv is not None and 0 < iv < 2:
            strikes.append(row["strike"])
            vols.append(iv)
    print("ATM example:")
    print("Strike:", row["strike"])
    print("Mid price:", row["mid"])
    print("Intrinsic:", max(S - row["strike"], 0))
    
    return strikes, vols


def plot_smile(strikes, implied_vols):
    plt.figure(figsize=(8,5))
    plt.plot(strikes, implied_vols, marker="o")
    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.title("Volatility Smile")
    plt.show()