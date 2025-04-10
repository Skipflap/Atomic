from models.BlackScholesModel import BlackScholesModel, Greeks, implied_volatility_call


def main():
    try:
        # Input parameters for the option
        S = float(input("Enter the current stock price (S): "))
        X = float(input("Enter the strike price (X): "))
        T = float(input("Enter the time to expiration in months (T): "))
        T = T / 12  # convert months to years
        r = float(input("Enter the risk-free interest rate (r) in decimal form: "))
        sigma = float(input("Enter the volatility (sigma) in decimal form: "))

        # Make dividend yield optional
        q_input = input(
            "Enter the continuous dividend yield (q) in decimal form (default is 0): "
        )
        q = float(q_input) if q_input else 0.0

        # Create the Black-Scholes model instance and compute prices/Greeks
        model = BlackScholesModel(S, X, T, r, sigma, q)
        greeks = Greeks(model)

        print(f"\nTheoretical Prices:")
        print(f"  Call Price: {model.call_price():.2f}")
        print(f"  Put Price:  {model.put_price():.2f}\n")

        print("Greeks:")
        delta = greeks.delta()
        theta = greeks.theta()
        rho = greeks.rho()

        print(f"  Delta (Call): {delta['call']:.4f}")
        print(f"  Delta (Put):  {delta['put']:.4f}")
        print(f"  Gamma:        {greeks.gamma():.4f}")
        print(f"  Theta (Call): {theta['call']:.4f}")
        print(f"  Theta (Put):  {theta['put']:.4f}")
        print(f"  Vega:         {greeks.vega():.4f}")
        print(f"  Vomma:        {greeks.vomma():.4f}")
        print(f"  Vanna:        {greeks.vanna():.4f}")
        print(f"  Rho (Call):   {rho['call']:.4f}")
        print(f"  Rho (Put):    {rho['put']:.4f}")

        # Real Market vs. Theoretical Price Comparison:
        market_call_price = float(input("\nEnter the observed market call price: "))
        theoretical_call_price = model.call_price()
        price_diff = market_call_price - theoretical_call_price

        print(f"\nComparison:")
        print(f"  Theoretical Call Price: {theoretical_call_price:.2f}")
        print(f"  Market Call Price:      {market_call_price:.2f}")

        if price_diff > 0:
            print(
                "  The option appears OVERVALUED (market price is higher than theoretical)."
            )
        elif price_diff < 0:
            print(
                "  The option appears UNDERVALUED (market price is lower than theoretical)."
            )
        else:
            print("  The market price is in line with the theoretical price.")

        # Solve for implied volatility
        implied_vol = implied_volatility_call(S, X, T, r, q, market_call_price)
        print(f"\nImplied Volatility: {implied_vol:.4f}")

        # Optionally, you could compare this IV to your input sigma or historical values.
        print(f"Input Volatility:   {sigma:.4f}")

    except ValueError:
        print("Invalid input. Please enter numeric values.")


if __name__ == "__main__":
    main()
