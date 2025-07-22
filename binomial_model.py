import numpy as np

def binomial_option_pricing(S, K, T, r, sigma, N, option_type='call', style='european'):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Final asset prices at maturity
    ST = np.array([S * (u**j) * (d**(N - j)) for j in range(N + 1)])

    # Option payoff at maturity
    if option_type == 'call':
        payoff = np.maximum(0, ST - K)
    else:
        payoff = np.maximum(0, K - ST)

    # Backward induction through tree
    for i in range(N - 1, -1, -1):
        payoff = np.exp(-r * dt) * (p * payoff[1:] + (1 - p) * payoff[:-1])
        if style == 'american':
            ST = np.array([S * (u**j) * (d**(i - j)) for j in range(i + 1)])
            if option_type == 'call':
                payoff = np.maximum(payoff, ST - K)
            else:
                payoff = np.maximum(payoff, K - ST)

    return payoff[0]
