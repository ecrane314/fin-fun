import numpy as np
from scipy.stats import norm

def black_scholes_expected_price(
    current_stock_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_interest_rate: float,
    volatility: float,
    option_type: str = 'call'
) -> float:
    """
    Calculates the Black-Scholes expected price for a European equity option.

    Args:
        current_stock_price (float): The current price of the underlying stock.
        strike_price (float): The strike price of the option.
        time_to_expiration_years (float): The time to expiration of the option in years.
        risk_free_interest_rate (float): The annualized risk-free interest rate (e.g., 0.05 for 5%).
        volatility (float): The annualized volatility of the stock's returns (e.g., 0.2 for 20%).
        option_type (str, optional): Type of the option, either 'call' or 'put'.
                                     Defaults to 'call'.

    Returns:
        float: The Black-Scholes expected price of the option.

    Raises:
        ValueError: If option_type is not 'call' or 'put'.
    """
    if option_type.lower() not in ['call', 'put']:
        raise ValueError("option_type must be either 'call' or 'put'")

    # Calculate d1 and d2
    d1 = (np.log(current_stock_price / strike_price) + \
          (risk_free_interest_rate + 0.5 * volatility**2) * time_to_expiration_years) / \
         (volatility * np.sqrt(time_to_expiration_years))
    d2 = d1 - volatility * np.sqrt(time_to_expiration_years)

    if option_type.lower() == 'call':
        # Calculate call option price
        option_price = (current_stock_price * norm.cdf(d1) - \
                        strike_price * np.exp(-risk_free_interest_rate * time_to_expiration_years) * norm.cdf(d2))
    else: # put option
        # Calculate put option price
        option_price = (strike_price * np.exp(-risk_free_interest_rate * time_to_expiration_years) * norm.cdf(-d2) - \
                        current_stock_price * norm.cdf(-d1))

    return option_price

if __name__ == '__main__':
    # Example Usage:
    S = 100  # Current stock price
    K = 105  # Strike price
    T = 0.5  # Time to expiration in years (6 months)
    r = 0.03 # Risk-free interest rate (3%)
    sigma = 0.25 # Volatility (25%)

    call_price = black_scholes_expected_price(S, K, T, r, sigma, option_type='call')
    put_price = black_scholes_expected_price(S, K, T, r, sigma, option_type='put')

    print(f"Current Stock Price (S): ${S:.2f}")
    print(f"Strike Price (K): ${K:.2f}")
    print(f"Time to Expiration (T): {T} years")
    print(f"Risk-Free Rate (r): {r*100:.2f}%")
    print(f"Volatility (sigma): {sigma*100:.2f}%")
    print(f"\nCalculated Call Option Price: ${call_price:.2f} 📞")
    print(f"Calculated Put Option Price: ${put_price:.2f} 📉")

    # Example with different parameters
    S2 = 50
    K2 = 48
    T2 = 1
    r2 = 0.01
    sigma2 = 0.30

    call_price2 = black_scholes_expected_price(S2, K2, T2, r2, sigma2, 'call')
    put_price2 = black_scholes_expected_price(S2, K2, T2, r2, sigma2, 'put')

    print(f"\n--- Another Example ---")
    print(f"Current Stock Price (S): ${S2:.2f}")
    print(f"Strike Price (K): ${K2:.2f}")
    print(f"Time to Expiration (T): {T2} years")
    print(f"Risk-Free Rate (r): {r2*100:.2f}%")
    print(f"Volatility (sigma): {sigma2*100:.2f}%")
    print(f"\nCalculated Call Option Price: ${call_price2:.2f} 📞")
    print(f"Calculated Put Option Price: ${put_price2:.2f} 📉")