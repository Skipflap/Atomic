from numpy import log, sqrt, exp
from scipy.stats import norm

class BlackScholesModel:
    def __init__(self, S, X, T, r, sigma, q=0.0):
        self.S = S
        self.X = X
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q

        self.d1 = (log(S / X) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        self.d2 = self.d1 - sigma * sqrt(T)

    def call_price(self):
        return self.S * exp(-self.q * self.T) * norm.cdf(self.d1) - self.X * exp(-self.r * self.T) * norm.cdf(self.d2)

    def put_price(self):
        return self.X * exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * exp(-self.q * self.T) * norm.cdf(-self.d1)

class Greeks:
    def __init__(self, model: BlackScholesModel):
        self.model = model
        self.pdf_d1 = norm.pdf(model.d1)

    def delta(self):
        return {
            "call": norm.cdf(self.model.d1),
            "put": norm.cdf(self.model.d1) - 1
        }

    def gamma(self):
        return self.pdf_d1 / (self.model.S * self.model.sigma * sqrt(self.model.T))

    def theta(self):
        S, X, T, r, sigma, q = self.model.S, self.model.X, self.model.T, self.model.r, self.model.sigma, self.model.q
        d1, d2 = self.model.d1, self.model.d2
        theta_call = (-S * exp(-q * T) * self.pdf_d1 * sigma / (2 * sqrt(T)) 
                      - r * X * exp(-r * T) * norm.cdf(d2)
                      + q * S * exp(-q * T) * norm.cdf(d1))
        theta_put = (-S * exp(-q * T) * self.pdf_d1 * sigma / (2 * sqrt(T)) 
                     + r * X * exp(-r * T) * norm.cdf(-d2)
                     - q * S * exp(-q * T) * norm.cdf(-d1))
        return {"call": theta_call, "put": theta_put}

    def vega(self):
        return self.model.S * exp(-self.model.q * self.model.T) * self.pdf_d1 * sqrt(self.model.T)
    
    def vomma(self):
        return self.vega() * ((self.model.d1 * self.model.d2) - 1) / self.model.sigma

    def vanna(self):
        return -self.model.S * exp(-self.model.q * self.model.T) * self.pdf_d1 * self.model.d2 / self.model.sigma

    def rho(self):
        X, T, r = self.model.X, self.model.T, self.model.r
        d2 = self.model.d2
        rho_call = X * T * exp(-r * T) * norm.cdf(d2)
        rho_put = -X * T * exp(-r * T) * norm.cdf(-d2)
        return {"call": rho_call, "put": rho_put}

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