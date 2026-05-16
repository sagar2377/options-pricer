# Options Pricing Engine

A Black-Scholes options pricing engine built from scratch in Python.

## What it does
- Computes call and put prices using the Black-Scholes formula
- Calculates all 5 Greeks: Delta, Gamma, Vega, Theta, Rho
- Visualises how each Greek behaves as stock price changes

## Formulas
- Black-Scholes call: S × N(d1) - K × e^(-rT) × N(d2)
- Black-Scholes put: K × e^(-rT) × N(-d2) - S × N(-d1)
- d1 = (ln(S/K) + (r + σ²/2) × T) / (σ × √T)
- d2 = d1 - σ × √T


## Sanity Check
With S=100, K=100, T=1, r=0.05, σ=0.2:
- Call price: 10.45, Put price: 5.57
- Delta: 0.637, Gamma: 0.0188, Vega: 37.52, Theta: -6.41, Rho: 53.23

## What I learned
- Delta follows an S-curve — near 0 deep OTM, 0.5 ATM, 1 deep ITM
- Gamma peaks at ATM where Delta is changing fastest
- Vega peaks at ATM where uncertainty and volatility sensitivity is highest
- Theta is most negative at ATM where time value is highest
- Rho keeps increasing with stock price unlike other Greeks — deeper ITM means more certain to exercise

## Greeks Dashboard
![Greeks Dashboard](greeks_dashboard.png)

## Tech Stack
- Python
- NumPy, Matplotlib

## Monte Carlo Pricing
- Simulates 10,000 stock price paths using Geometric Brownian Motion
- Calculates call/put payoffs across all paths and averages them
- Discounts average payoff to present value using e^(-rT)
- Converges to Black-Scholes price with enough simulations (100,000 paths gives ~10.47 vs BS 10.45)

## Implied Volatility Solver
- Takes a market option price as input
- Uses Newton-Raphson method with Vega as the derivative to converge efficiently
- Typically converges in 5-10 iterations
- Example: implied_vol(10.45, 100, 100, 1, 0.05) → 0.1999 ≈ 0.2

## Volatility Surface
- Pulled real AAPL options chain data using yfinance
- Calculated implied volatility across 6 expiry dates and strikes from $100-$300
- Plotted 3D volatility surface showing both the volatility skew and term structure
![Volatility Surface](vol_surface.png)