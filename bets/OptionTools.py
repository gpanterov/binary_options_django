import numpy as np
import random
from scipy.stats import norm
from bets.models import PlacedBets, AssetPrices

def cash_or_nothing(S, K, T, vol, option_type):
	"""
	Return the value of a cash or nothing call

	References:
	-----------
	http://en.wikipedia.org/wiki/Binary_option#Black.E2.80.93Scholes_valuation
	"""
	d1 = (np.log(S/K) + T * 0.5 * vol**2) / (vol * T**0.5)
	d2 = d1 - vol * T**0.5
	if option_type == "call":
		return norm.cdf(d2)
	elif option_type == "put":
		return norm.cdf(-d2)
	else:
		print "Incorrectly specifed option type. Must be either *call* or *put*"
		return None


def option_params(expire, option_start_price, current_time, current_price):
	"""
	Calculates and returns some useful parameters of the options like strike prices (fixed for the life of the option)
	and the payouts, given the time and prices
	"""

	time_remaining = expire - current_time
	if option_start_price == 0 or option_start_price is None:
		print "Problem with Option Price", option_start_price
		option_start_price = current_price


	print "Option Start Price is: ", option_start_price
	call_strike1 = round(option_start_price - 0.0002, 4)
	call_strike2 = round(option_start_price, 4)
	call_strike3 = round(option_start_price + 0.0002, 4)
	call_strike4 = round(option_start_price + 0.0005, 4)
	call_strike5 = round(option_start_price + 0.0010, 4)

	call_payout1 = round(1 + random.random(),2)
	call_payout2 = round(random.random() + call_payout1,2)
	call_payout3 = round(random.random() + call_payout2,2)
	call_payout4 = round(random.random() + call_payout3,2)
	call_payout5 = round(random.random() + call_payout4,2)

	put_strike1 = round(option_start_price + 0.0002, 4)
	put_strike2 = round(option_start_price, 4)
	put_strike3 = round(option_start_price - 0.0002, 4)
	put_strike4 = round(option_start_price - 0.0005, 4)
	put_strike5 = round(option_start_price - 0.0010, 4)


	put_payout1 = round(1 + random.random(),2)
	put_payout2 = round(random.random() + put_payout1,2)
	put_payout3 = round(random.random() + put_payout2,2)
	put_payout4 = round(random.random() + put_payout3,2)
	put_payout5 = round(random.random() + put_payout4,2)



	return call_strike1, call_strike2,  call_strike3, call_strike4, call_strike5, \
			call_payout1, call_payout2, call_payout3,call_payout4,call_payout5,\
			put_strike1, put_strike2, put_strike3,put_strike4,put_strike5,\
			put_payout1, put_payout2,put_payout3,put_payout4,put_payout5

def get_price(timestamp):
	"""
	Calculate the price for a given time stamp
	"""
	found_price = False
	counter = 0

	if AssetPrices.objects.latest('time').time < timestamp:
		# Attempting to find the price of a future date	
		print "You must wait a bit ", AssetPrices.objects.latest('time').time - timestamp
		return None

	while not found_price:
		counter +=1
		try:
			price = AssetPrices.objects.get(time=timestamp)
			found_price = True
		except KeyboardInterrupt:
			raise
		except:
			timestamp -= 1
		if counter > 20:
			return 0
	return price.eurusd

