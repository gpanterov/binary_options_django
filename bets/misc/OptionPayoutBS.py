import numpy as np
import pandas as pd
from scipy.stats import norm

# Parameters
S = 370.  # current price
K = 300.  # strike
T = 15   # Time to maturity
vol = 0.05  # volatility


def CON_call(S, K, T, vol):
	"""
	Return the value of a cash or nothing call

	References:
	-----------
	http://en.wikipedia.org/wiki/Binary_option#Black.E2.80.93Scholes_valuation
	"""
	d1 = (np.log(S/K) + T * 0.5 * vol**2) / (vol * T**0.5)
	d2 = d1 - vol * T**0.5
	return norm.cdf(d2)

def brownian(S, T, vol):
	"""
	Returns the price of an asset with starting price S after T periods.
	The returns are assumed normal with mean zero and volatility *vol*
	"""
	Snew = S
	for i in range(T):
		ret = np.random.normal(0, vol)
		Snew = Snew * (1 + ret)
		#Snew = Snew + ret

	#return np.exp(Snew)	
	return Snew


def simulate_bin_call(S, K, T, vol, Nsim):
	"""
	Run *Nsim* simulations of Brownian motions and calculate
	the share of times that a binary call would have paid out
	"""
	end_prices = []
	for i in range(int(Nsim)):
		price = brownian(S, T, vol)
		end_prices.append(price)

	end_prices = np.array(end_prices)
	prob = 1. * np.sum(end_prices > K) / Nsim
	return prob

BS_price = CON_call(S, K, T, vol)

sim_prob = simulate_bin_call(S, K, T, vol, 1e5)

print "Black-Scholes price is %s || The simulation probability is %s" % (BS_price, sim_prob)
