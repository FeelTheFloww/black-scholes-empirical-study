# black_scholes/main.py

import yfinance as yf
from datetime import datetime

from Black_Scholes.data_loader import load_option_chain
from Black_Scholes.model import call_price
from Black_Scholes.smile import compute_smile, plot_smile
from Black_Scholes.validation import (
    compare_implied_vol,
    put_call_parity_test,
    sanity_checks
)

ticker_symbol = "SPY"
r = 0.02

# --- Load option chains
option_data = load_option_chain(ticker_symbol)

# --- Spot (fix FutureWarning)
tkr = yf.Ticker(ticker_symbol)
S = tkr.history(period="1d")["Close"].iloc[-1]

# --- Pick a suitable expiration (30-90 days)
expirations = list(option_data.keys())
valid_exps = []

for exp_candidate in expirations:
    expiration = datetime.strptime(exp_candidate, "%Y-%m-%d")
    T_tmp = (expiration - datetime.today()).days / 365.25
    if 0.08 < T_tmp < 0.25:
        valid_exps.append((exp_candidate, T_tmp))

if not valid_exps:
    raise ValueError("No suitable expiration found.")

exp, T = valid_exps[0]

# --- Use the matching chain
df = option_data[exp].copy()
df["mid"] = (df["bid"] + df["ask"]) / 2

print("Using expiration:", exp)
print("First contract symbols:")
print(df["contractSymbol"].head())
print("T (years):", T)
print("S =", S)

# --- ATM debug
df["distance"] = (df["strike"] - S).abs()
atm_row = df.loc[df["distance"].idxmin()]

test_sigma = 0.2
K_test = float(atm_row["strike"])
price_model = call_price(S, K_test, T, r, test_sigma)

print("\nATM contract:")
print(atm_row[["contractSymbol", "strike", "bid", "ask", "mid", "impliedVolatility"]])
print("BS price with 20% vol:", price_model)

# --- Validation
iv_report = compare_implied_vol(df, S, T, r)
print("\nIV Validation Report:", iv_report)

chain = tkr.option_chain(exp)
parity_report = put_call_parity_test(chain.calls, chain.puts, S, T, r)
print("Put-Call Parity Report:", parity_report)

sanity = sanity_checks(S, K_test, T, r)
print("Sanity Checks:", sanity)

# --- Smile
strikes, vols = compute_smile(df, S, T, r)
plot_smile(strikes, vols)