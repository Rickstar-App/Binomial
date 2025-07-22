import numpy as np
from binomial_model import binomial_option_pricing

def calculate_greeks(S, K, T, r, sigma, N, option_type='call', style='european'):
    eps = 0.01

    # Delta
    price_up = binomial_option_pricing(S + eps, K, T, r, sigma, N, option_type, style)
    price_down = binomial_option_pricing(S - eps, K, T, r, sigma, N, option_type, style)
    delta = (price_up - price_down) / (2 * eps)

    # Gamma
    price_mid = binomial_option_pricing(S, K, T, r, sigma, N, option_type, style)
    gamma = (price_up - 2 * price_mid + price_down) / (eps ** 2)

    # Vega
    price_vega_up = binomial_option_pricing(S, K, T, r, sigma + eps, N, option_type, style)
    price_vega_down = binomial_option_pricing(S, K, T, r, sigma - eps, N, option_type, style)
    vega = (price_vega_up - price_vega_down) / (2 * eps)

    # Theta
    price_theta_up = binomial_option_pricing(S, K, T + eps, r, sigma, N, option_type, style)
    theta = (price_theta_up - price_mid) / eps

    # Rho
    price_rho_up = binomial_option_pricing(S, K, T, r + eps, sigma, N, option_type, style)
    price_rho_down = binomial_option_pricing(S, K, T, r - eps, sigma, N, option_type, style)
    rho = (price_rho_up - price_rho_down) / (2 * eps)

    return {
        'delta': round(delta, 4),
        'gamma': round(gamma, 4),
        'vega': round(vega, 4),
        'theta': round(theta, 4),
        'rho': round(rho, 4)
    }