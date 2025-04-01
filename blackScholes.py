from numpy import log, sqrt, exp
from scipy.stats import norm


def black_scholes(S, X, T, r, sigma):
    """
    Parameters:
    - S: Current price
    - X: Strike price
    - T: Time to expiration(in years)
    - r: Risk-free interest rate (annual rate, in decimal form)
    - sigma: Volatility of the underlying asset (annualized, in decimal form)
    """

    """
    Returns:
    - call_price: Theoretical price of call option
    - put_price: Theoretical price of put option
    """

    d1 = (log(S / X) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    put_price = X * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    call_price = (
        S * norm.cdf(d1) - (X * exp(-(r * T)) * norm.cdf(d2)) - S * norm.cdf(-d1)
    )

    return put_price, call_price


def main():
    try:
        S = float(input("Enter the current stock price (S): "))
        X = float(input("Enter the strike price (X): "))
        T = float(input("Enter the time to expiration in years (T): "))
        r = float(
            input(
                "Enter the risk-free interest rate (r) in decimal form (e.g., 0.05 for 5%): "
            )
        )
        sigma = float(
            input("Enter the volatility (sigma) in decimal form (e.g., 0.2 for 20%): ")
        )
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    call_price, put_price = black_scholes(S, X, T, r, sigma)
    print(f"European Call Option Price: {call_price:.2f}")
    print(f"European Put Option Price: {put_price:.2f}")


if __name__ == "__main__":
    main()
