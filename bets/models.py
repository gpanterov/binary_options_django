from django.db import models
from django.contrib.auth.models import User
# went back a commit c34222a2050b9d1f1e8b995de3058cd1ad0d4ddf



class PlacedBets(models.Model):
	user = models.CharField(max_length=30,null=True)
	option_asset = models.CharField(max_length=10,null=True)
	bet_type = models.CharField(max_length=10,null=True)
	bet_time = models.IntegerField(default=0, null=True)  # Unix time for the bet
	bet_size = models.IntegerField(default=0, null=True)  # Size of bet in satoshis
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




# Add Deposit/Funds model
class Deposits(models.Model):
	username = models.CharField(max_length=30,null=True)
	time = models.IntegerField(default=0)
	size = models.IntegerField(default=0, null=True)  # Size of bet in satoshis
	def __unicode__(self):
		return self.username

class Balances(models.Model):
	username = models.CharField(max_length=30,null=True)
	balance = models.IntegerField(default=0)
	def __unicode__(self):
		return self.username

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
