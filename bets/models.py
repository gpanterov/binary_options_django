from django.db import models
from django.contrib.auth.models import User
# went back a commit c34222a2050b9d1f1e8b995de3058cd1ad0d4ddf



class PlacedBets(models.Model):
	user = models.CharField(max_length=30,null=True)
	option_asset = models.CharField(max_length=10,null=True)
	bet_type = models.CharField(max_length=10,null=True)
	bet_time = models.IntegerField(default=0, null=True)  # Unix time for the bet
	bet_size = models.FloatField(default=0, null=True)  # Size of bet in satoshis
	bet_strike = models.FloatField(default=0, null=True)
	bet_payout = models.FloatField(default=0, null=True)
	option_expire = models.IntegerField(default=0, null=True)
	bet_outcome = models.CharField(max_length=10, null=True)

	price_at_expiration = models.FloatField(default=0, null=True)
	def __unicode__(self):
		return self.user

class AssetPrices(models.Model):
	time = models.IntegerField(default=0)
	eurusd = models.FloatField(default=0, null=True)
	usdjpy = models.FloatField(default=0, null=True)
	usdchf = models.FloatField(default=0, null=True)
	eurchf = models.FloatField(default=0, null=True)

	oil = models.FloatField(default=0, null=True)
	gold = models.FloatField(default=0, null=True)

	
	spx500 = models.FloatField(default=0, null=True)
	ftse100 = models.FloatField(default=0, null=True)
	nikkei = models.FloatField(default=0, null=True)

# Add Deposit/Funds model
class Deposits(models.Model):
	transaction_hash = models.CharField(max_length=90,null=True)
	input_address = models.CharField(max_length=50,null=True)
	username = models.CharField(max_length=30,null=True)
	confirmations = models.IntegerField(default=0)
	time = models.IntegerField(default=0)
	size = models.FloatField(default=0, null=True)  # Size of bet in bitcoins
	included = models.BooleanField(default=False)  # Has this deposit been included towards the balance
	def __unicode__(self):
		return self.username

class Balances(models.Model):
	username = models.CharField(max_length=30,null=True)
	balance = models.FloatField(default=0)
	def __unicode__(self):
		return self.username

class Promos(models.Model):
	code = models.CharField(max_length=30,null=True)
	used = models.BooleanField(default=False)
	value = models.FloatField(default=0, null=True) 
	user = models.CharField(max_length=30,null=True)

	def __unicode__(self):
		return self.code


class Volatility(models.Model):

	time = models.IntegerField(default=0)
	vol_eurusd = models.FloatField(default=1, null=False)
	vol_usdjpy = models.FloatField(default=1, null=False)

	vol_eurchf = models.FloatField(default=1, null=False)
	vol_gold = models.FloatField(default=1, null=False)
	vol_oil = models.FloatField(default=1, null=False)
	vol_sp500 = models.FloatField(default=1, null=False)
	vol_nikkei = models.FloatField(default=1, null=False)


class Average(models.Model):

	time = models.IntegerField(default=0)
	avg_eurusd = models.FloatField(default=1, null=False)
	avg_usdjpy = models.FloatField(default=1, null=False)

	avg_eurchf = models.FloatField(default=1, null=False)
	avg_gold = models.FloatField(default=1, null=False)
	avg_oil = models.FloatField(default=1, null=False)
	avg_sp500 = models.FloatField(default=1, null=False)
	avg_nikkei = models.FloatField(default=1, null=False)

# Add Last time checked for settled transactions
