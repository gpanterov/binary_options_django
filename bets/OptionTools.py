import numpy as np
import random
from scipy.stats import norm
from bets.models import PlacedBets, AssetPrices
import time
import urllib2

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


def get_bet_outcome(bet):
	"""
	Return the outcome of a bet at a given timestamp
	"""
	timestamp = int(time.time())
	if bet.bet_time > timestamp:
		return "Error (Bet made after timestamp)", 0
	if bet.option_expire > timestamp:
		return "Pending", 0
	else:
		exp_price, latest_available_time = get_closest_prices(bet.option_asset, bet.option_expire)
		if bet.option_expire - latest_available_time > 10:
			print "The latest available price is at least 10 seconds before the option expiration time"
			return "Unknown"
		res = evaluate_option(bet.bet_type, exp_price, bet.bet_strike)
		if res:
			return "Success", exp_price
		else:
			return "Loss", exp_price


def evaluate_option(option_type, exp_price, strike_price):
	"""
	Find out if an option is success or loss for a given type,
	price and strike
	"""
	if option_type == "CALL" and exp_price > strike_price:
		return True
	elif option_type == "CALL" and exp_price <= strike_price:
		return False
	elif option_type == "PUT" and exp_price >= strike_price:
		return False
	elif option_type == "PUT" and exp_price < strike_price:
		return True






def get_closest_prices(asset, timestamp):
	"""
	Returns the two instances of the AssetPrice class that are closest
	to timestamp (under it and over it)
	"""
	prices_before_timestamp = AssetPrices.objects.filter(time__lte = timestamp)
	#prices_after_timestamp = AssetPrices.objects.filter(time__gte = timestamp)
	if len(prices_before_timestamp)>0:
		closest_to_timestamp_under = prices_before_timestamp[len(prices_before_timestamp)-1]
	else:
		print "There is no data before time stamp. Possibly no price data has been collected or too low a timestamp"
		raise
	if asset == "EURUSD":
		price = closest_to_timestamp_under.eurusd
	elif asset == "USDJPY":
		price = closest_to_timestamp_under.usdjpy
	elif asset == "EURCHF":
		price = closest_to_timestamp_under.eurchf
	elif asset == "USDCHF":
		price = closest_to_timestamp_under.usdchf
	elif asset == "XAUUSD":
		price = closest_to_timestamp_under.gold
	elif asset == "USOil":
		price = closest_to_timestamp_under.oil
	elif asset == "SPX500":
		price = closest_to_timestamp_under.spx500
	elif asset == "JPN225":
		price = closest_to_timestamp_under.nikkei
	elif asset == "UK100":
		price = closest_to_timestamp_under.ftse100
	else:
		print "Error (Unknown asset)"
		raise

	return price, closest_to_timestamp_under.time



def send_money(to, amount):
	guid = 'd99c232a-2ab7-4371-ad4b-ad8b8aa74008'
	main_password='diamondbook932'
	url = "https://blockchain.info/merchant/" + guid + "/payment?password=" + main_password + \
			"&to=" + to + "&amount=" + amount

	r = urllib2.urlopen(url)
	return r


