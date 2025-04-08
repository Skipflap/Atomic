from models.BlackScholesModel import BlackScholesModel, Greeks

def main():
    try:
        S = float(input("Enter the current stock price (S): "))
        X = float(input("Enter the strike price (X): "))
        T = float(input("Enter the time to expiration in months (T): "))
        T = T / 12  # Convert months to years
        r = float(input("Enter the risk-free interest rate (r) in decimal form: "))
        sigma = float(input("Enter the volatility (sigma): "))
        q_input = input("Enter the continuous dividend yield (q) in decimal form (default is 0): ")
        q = float(q_input) if q_input else 0.0

        model = BlackScholesModel(S, X, T, r, sigma, q)
        greeks = Greeks(model)

        print(f"\nCall Price: {model.call_price():.2f}")
        print(f"Put Price:  {model.put_price():.2f}\n")

        print("Greeks:")
        delta = greeks.delta()
        theta = greeks.theta()
        rho = greeks.rho()

        print(f"Delta (Call): {delta['call']:.4f}")
        print(f"Delta (Put):  {delta['put']:.4f}")
        print(f"Gamma:        {greeks.gamma():.4f}")
        print(f"Theta (Call): {theta['call']:.4f}")
        print(f"Theta (Put):  {theta['put']:.4f}")
        print(f"Vega:         {greeks.vega():.4f}")
        print(f"Rho (Call):   {rho['call']:.4f}")
        print(f"Rho (Put):    {rho['put']:.4f}")
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    main()