import math

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