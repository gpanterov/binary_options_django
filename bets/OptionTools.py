import numpy as np
import random
from scipy.stats import norm
from bets.models import PlacedBets, AssetPrices
import time, datetime
import urllib2
import xmltodict

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

def calculate_asset_vol(asset):
	Nshort = 90
	default_vol = 1e-6

	
	all_asset_prices = AssetPrices.objects.filter(time__gte=time.time() - Nshort)
	if len(all_asset_prices) < 20:
		print "There are too few observations in the last %s seconds to calculate the volatility" %(Nshort)
		return None
	if asset == "EURUSD":
		price = [i.eurusd for i in all_asset_prices]
	elif asset == "USDJPY":
		price = [i.usdjpy for i in all_asset_prices]

	elif asset == "EURCHF":
		price = [i.eurchf for i in all_asset_prices]
	elif asset == "USDCHF":
		price = [i.usdchf for i in all_asset_prices]
	elif asset == "XAUUSD":
		price = [i.gold for i in all_asset_prices]
	elif asset == "USOil":
		price = [i.oil for i in all_asset_prices]
	elif asset == "SPX500":
		price = [i.spx500 for i in all_asset_prices]
	elif asset == "JPN225":
		price = [i.nikkei for i in all_asset_prices]
	elif asset == "UK100":
		price = [i.ftse100 for i in all_asset_prices]
	else:
		print "Error (Unknown asset)"
		raise
	price = np.log(price)
	price_delta = price[1:] - price[:-1]
	vol = np.std(price_delta)
	return vol



def calculate_option_payout(latest_price, strike, expiration, volatility, option_type):
	prob = cash_or_nothing(latest_price, strike, expiration, volatility, option_type)

	payout = 1/prob
	print "True payout is ", payout
	if payout <2.1 and payout>1.9:
		payout_profit_adj = payout - 0.06 * payout
		return round(payout_profit_adj,3)
	payout_profit_adj = payout - 0.15 * payout
	payout_profit_adj = min(payout_profit_adj, 10.)
	payout_profit_adj = max(payout_profit_adj, 1.)
	return round(payout_profit_adj, 3)



def scrape_price_now(asset):

	url = "http://rates.fxcm.com/RatesXML"
	try:
		r = urllib2.urlopen(url)
		timestamp = time.time()
		data = r.read()
		timestamp = time.time()
		xml = xmltodict.parse(data)
		if asset == "EURUSD":
			price = float(xml['Rates']['Rate'][0]['Bid'])
		elif asset == "USDJPY":
			price =float(xml['Rates']['Rate'][1]['Bid'])
		elif asset == "EURCHF":
			price = 	float(xml['Rates']['Rate'][4]['Bid'])
		elif asset == "USDCHF":
			price = float(xml['Rates']['Rate'][3]['Bid'])
		elif asset == "XAUUSD":
			price = float(xml['Rates']['Rate'][55]['Bid'])
		elif asset == "USOil":
			price = float(xml['Rates']['Rate'][53]['Bid'])
		elif asset == "SPX500":
			price = float(xml['Rates']['Rate'][43]['Bid'])
		elif asset == "JPN225":
			price = float(xml['Rates']['Rate'][51]['Bid'])
		elif asset == "UK100":
			price = float(xml['Rates']['Rate'][45]['Bid'])
		else:
			print "Error (Unknown asset)"
		return float(price)
	except:
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
		try:
			exp_price, latest_available_time = get_closest_prices(bet.option_asset, bet.option_expire)
		except:
			return "Pending", 0
		if bet.option_expire - latest_available_time > 10:
			print "The latest available price is at least 10 seconds before the option expiration time"
			return "Unknown", 0
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
	main_parola='Never_the_s4am3_aga1n' # THIS MUST BE CHANGED WHEN UPLOADED TO SERVER
	url = "https://blockchain.info/merchant/" + guid + "/payment?password=" + main_parola + \
			"&to=" + to + "&amount=" + amount

	r = urllib2.urlopen(url)
	return r

def check_open_markets(asset):
	if asset == "EURUSD" or asset=="EURCHF" or asset == "USDJPY" or asset=="USDCHF" or asset == "USOil" or asset =="XAUUSD":
		is_forex = True
	else:
		is_forex = False

	utc_now = datetime.datetime.utcnow()
	weekday = utc_now.weekday()
	hour = utc_now.hour
	minute = utc_now.minute
	if weekday >=5:
		msg = "Saturday and Sunday- markets are closed. All assets"
		return False, msg

	if is_forex:
		if weekday <4:
			msg = "Forex markets are open during the weekdays"
			return True, msg
		elif weekday == 4 and hour < 21:
			msg = "Forex. Friday before 4 EST"
			return True, msg
		else:
			msg = "Weekend - no trades. SHouldn't see this message"
			return False, msg

	if asset =="SPX500":
		if hour >= 13 and hour < 21:
			msg = "SPX500 is open"
			return True, msg
		else:
			return False, "SPX500 is closed"

	if asset == "UK100":
		if hour >= 8 and hour < 16:
			msg = "UK100 is open"
			return True, msg
		else:
			msg = "UK100 is closed"
			return False, msg

		pass
	if asset == "JPN225":
		if hour >=0 and hour < 7:
			msg = "JPN225 is open"
			return True, msg
		else:
			return False, "Nikkei closed"
	return False, "None"



def get_latest_price_from_db(asset, latest):
	"""
	"""
	#prices_after_timestamp = AssetPrices.objects.filter(time__gte = timestamp)
	if asset == "EURUSD":
		price = latest.eurusd
	elif asset == "USDJPY":
		price = latest.usdjpy
	elif asset == "EURCHF":
		price = latest.eurchf
	elif asset == "USDCHF":
		price = latest.usdchf
	elif asset == "XAUUSD":
		price = latest.gold
	elif asset == "USOil":
		price = latest.oil
	elif asset == "SPX500":
		price = latest.spx500
	elif asset == "JPN225":
		price = latest.nikkei
	elif asset == "UK100":
		price = latest.ftse100
	else:
		print "Error (Unknown asset)"
		raise

	return price

def transform_in_pips(val, asset):
	if asset == "EURUSD":
		price = val * 10000
	elif asset == "USDJPY":
		price = val * 100
	elif asset == "EURCHF":
		price = val * 10000
	elif asset == "USDCHF":
		price = val * 10000
	elif asset == "XAUUSD":
		price = val * 100
	elif asset == "USOil":
		price = val * 100
	elif asset == "SPX500":
		price = val * 10
	elif asset == "JPN225":
		price = val
	elif asset == "UK100":
		price = val
	else:
		print "Error (Unknown asset)"
		raise

	return round(price)

