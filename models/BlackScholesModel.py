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

        # Use dividend yield q in the drift term:
        self.d1 = (log(S / X) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
        self.d2 = self.d1 - sigma * sqrt(T)

    def call_price(self):
        return self.S * exp(-self.q * self.T) * norm.cdf(self.d1) - self.X * exp(
            -self.r * self.T
        ) * norm.cdf(self.d2)

    def put_price(self):
        return self.X * exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * exp(
            -self.q * self.T
        ) * norm.cdf(-self.d1)


class Greeks:
    def __init__(self, model: BlackScholesModel):
        self.model = model
        self.pdf_d1 = norm.pdf(model.d1)

    def delta(self):
        return {"call": norm.cdf(self.model.d1), "put": norm.cdf(self.model.d1) - 1}

    def gamma(self):
        return self.pdf_d1 / (self.model.S * self.model.sigma * sqrt(self.model.T))

    def theta(self):
        S, X, T, r, sigma, q = (
            self.model.S,
            self.model.X,
            self.model.T,
            self.model.r,
            self.model.sigma,
            self.model.q,
        )
        d1, d2 = self.model.d1, self.model.d2
        theta_call = (
            -S * exp(-q * T) * self.pdf_d1 * sigma / (2 * sqrt(T))
            - r * X * exp(-r * T) * norm.cdf(d2)
            + q * S * exp(-q * T) * norm.cdf(d1)
        )
        theta_put = (
            -S * exp(-q * T) * self.pdf_d1 * sigma / (2 * sqrt(T))
            + r * X * exp(-r * T) * norm.cdf(-d2)
            - q * S * exp(-q * T) * norm.cdf(-d1)
        )
        return {"call": theta_call, "put": theta_put}

    def vega(self):
        return (
            self.model.S
            * exp(-self.model.q * self.model.T)
            * self.pdf_d1
            * sqrt(self.model.T)
        )

    def vomma(self):
        # Vomma measures the sensitivity of Vega to changes in volatility.
        return self.vega() * ((self.model.d1 * self.model.d2) - 1) / self.model.sigma

    def vanna(self):
        # Vanna measures the sensitivity of Delta to changes in volatility.
        return (
            -self.model.S
            * exp(-self.model.q * self.model.T)
            * self.pdf_d1
            * self.model.d2
            / self.model.sigma
        )

    def rho(self):
        X, T, r = self.model.X, self.model.T, self.model.r
        d2 = self.model.d2
        rho_call = X * T * exp(-r * T) * norm.cdf(d2)
        rho_put = -X * T * exp(-r * T) * norm.cdf(-d2)
        return {"call": rho_call, "put": rho_put}


def implied_volatility_call(
    S, X, T, r, q, market_call_price, initial_guess=0.2, tol=1e-6, max_iter=100
):
    """
    Computes the implied volatility for a European call option using the Newton-Raphson method.

    Parameters:
      - S: Current stock price
      - X: Strike price
      - T: Time to expiration (in years)
      - r: Risk-free interest rate (in decimal form)
      - q: Continuous dividend yield (in decimal form)
      - market_call_price: Observed market price of the call option
      - initial_guess: Initial volatility guess (default 0.2 for 20%)
      - tol: Tolerance for convergence (default 1e-6)
      - max_iter: Maximum number of iterations (default 100)

    Returns:
      - The implied volatility (sigma) that makes the theoretical call price match the market_call_price.
    """
    sigma = initial_guess
    for i in range(max_iter):
        # Create a temporary model instance with the current volatility guess
        model = BlackScholesModel(S, X, T, r, sigma, q)
        price = model.call_price()
        diff = price - market_call_price

        if abs(diff) < tol:
            return sigma

        greeks = Greeks(model)
        vega_val = greeks.vega()
        if vega_val == 0:
            break

        sigma = sigma - diff / vega_val

    return sigma
