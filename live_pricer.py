# live_pricer.py
import time
from config import API_KEY
from data_provider import get_latest_intraday_price
from models.BlackScholesModel import BlackScholesModel, Greeks, implied_volatility_call

# Option parameters (could also be CLI args)
SYMBOL = "AAPL"
STRIKE = 170.0
DAYS_TO_EXPIRY = 30
T = DAYS_TO_EXPIRY / 252                          # Trading days fraction :contentReference[oaicite:9]{index=9}
R = 0.01                                         # 1% risk-free
Q = 0.0                                          # No dividend

def main():
    print(f"Starting live pricer for {SYMBOL}, strike={STRIKE}, T={T:.4f}")
    try:
        while True:
            S = get_latest_intraday_price(SYMBOL, interval='1min')
            model = BlackScholesModel(S, STRIKE, T, R, sigma=0.2, q=Q)
            theo_call = model.call_price()
            greeks = Greeks(model)
            iv = implied_volatility_call(S, STRIKE, T, R, Q, market_call_price=theo_call)

            print(f"S={S:.2f} | TheoCall={theo_call:.2f} | IV={iv:.2%}")
            print(f"  Δ_call={greeks.delta()['call']:.4f}, Γ={greeks.gamma():.4f}, ν={greeks.vega():.4f}")
            print("—" * 60)

            time.sleep(60)  # pause 1 minute to respect rate limits :contentReference[oaicite:10]{index=10}

    except KeyboardInterrupt:
        print("Live pricer stopped.")

if __name__ == "__main__":
    main()
