import numpy as np
import random
from bets.models import PlacedBets, AssetPrices, OfferedOptions
def option_params(option_start_time, expire, option_start_price, current_time, current_price):
	"""
	Calculates and returns some useful parameters of the options like strike prices (fixed for the life of the option)
	and the payouts, given the time and prices
	"""
	call_strike1 = round(option_start_price + 0.0002, 4)
	call_strike2 = round(option_start_price + 0.0005, 4)
	time_remaining = expire - current_time
	call_payout1 = round(call_strike1 - current_price + 4. / time_remaining, 4)
	call_payout2 = round(call_strike2 - current_price + 3. / time_remaining, 4)


	put_strike1 = round(option_start_price - 0.0002, 4)
	put_strike2 = round(option_start_price - 0.0005, 4)
	put_payout1 = round(put_strike1 - current_price + 3. / time_remaining, 4)
	put_payout2 = round(put_strike2 - current_price + 2. / time_remaining, 4)


	return call_strike1, call_strike2, call_payout1, call_payout2,\
			put_strike1, put_strike2, put_payout1, put_payout2

def get_price(timestamp):
	"""
	Calculate the price for a given time stamp
	"""
	found_price = False
	counter = 0

	if AssetPrice.objects.latest('time').time < timestamp:
		# Attempting to find the price of a future date	
		print "You must wait a bit"
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

