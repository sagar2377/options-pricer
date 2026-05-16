import math
import numpy as np

# -------------------------
# Normal CDF
# -------------------------
def N(x):
    return 0.5*(1+math.erf(x/math.sqrt(2)))
# -------------------------
# Normal PDF
# -------------------------
def N_prime(x):
    return math.exp(-x**2/2)/math.sqrt(2*math.pi)


# -------------------------
# d1
# -------------------------
def d1(S, K, T, r, sigma):
   bot = sigma*math.sqrt(T)
   top = math.log(S/K) + (r+0.5*sigma**2)*T
   return top/bot


# -------------------------
# d2
# -------------------------
def d2(S, K, T, r, sigma):
    d = d1(S, K, T, r, sigma)
    return d - sigma*math.sqrt(T)


# -------------------------
# Call option price
# -------------------------
def call_price(S, K, T, r, sigma):
    C = S*N(d1(S, K, T, r, sigma))- K*math.exp(-r*T)* N(d2(S, K, T, r, sigma))
    return C


# -------------------------
# Put option price
# -------------------------
def put_price(S, K, T, r, sigma):
    P = - S*N(-d1(S, K, T, r, sigma))+ K*math.exp(-r*T)* N(-d2(S, K, T, r, sigma))
    return P

def delta(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return N(d1(S, K, T, r, sigma))
    else:
        return  N(d1(S, K, T, r, sigma)) -1 

def gamma(S, K, T, r, sigma):
    top =  N_prime(d1(S, K, T, r, sigma))
    bot = S*sigma*math.sqrt(T)
    return top/bot

def vega(S, K, T, r, sigma):
    return S * N_prime(d1(S, K, T, r, sigma))*math.sqrt(T)


def theta(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        theta = (-S*N_prime(d1(S, K, T, r, sigma))*sigma)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*N(d2(S, K, T, r, sigma))
    else:
        theta = (-S*N_prime(d1(S, K, T, r, sigma))*sigma)/(2*math.sqrt(T)) + r*K*math.exp(-r*T)*N(-d2(S, K, T, r, sigma))
    return theta 

def rho(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return K*T*math.exp(-r*T)*N(d2(S, K, T, r, sigma))
    else:
        return - K*T*math.exp(-r*T)*N(-d2(S, K, T, r, sigma))

def simulate_path(S, r, sigma, T, steps):
    cnt = 0
    S_curr = S
    dt = 1/steps
    while cnt <steps:
        z = np.random.normal()
        ##S = S × e^((r - 0.5 × σ²) × dt + σ × √dt × Z)
        S_next = S_curr*math.exp((r-0.5*sigma**2)*dt+sigma*math.sqrt(dt)*z)
        S_curr = S_next
        cnt +=1
    return S_next

def monte_carlo(S, K, T, r, sigma, option_type='call', simulations=10000, steps=252):
    cnt = 0
    payoffs =  []
    while cnt < simulations:
        S_final = simulate_path(S, r, sigma, T, steps)
        if option_type == 'call': #calc payoff for call
            payoff = max(S_final - K, 0)
        else: #calc payoff for put
            payoff = max(K - S_final, 0)
        payoffs.append(payoff)
        cnt += 1
    avg_payoff = np.mean(payoffs)
    price_curr = avg_payoff*math.exp(-r*T)
    return price_curr

def implied_vol(market_price, S, K, T, r, option_type='call'):
    sigma  = 0.2
    while True:
        if option_type == 'call':
            price_BS =  call_price(S, K, T, r, sigma)
        else:
            price_BS =  put_price(S, K, T, r, sigma)
        if np.isclose(market_price, price_BS):
            break
        V = vega(S, K, T, r, sigma)
        sigma = sigma - ( price_BS - market_price)/V
    return sigma
        