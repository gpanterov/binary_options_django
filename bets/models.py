from django.db import models as mls
from django.contrib.auth.models import User

class UserProfile(mls.Model):
	user = mls.OneToOneField(User)
	def __unicode__(self):
		return self.user.username


class PlacedBets(mls.Model):
	user = mls.CharField(max_length=30,null=True)
	option_asset = mls.CharField(max_length=10,null=True)
	bet_type = mls.CharField(max_length=10,null=True)
	bet_time = mls.IntegerField(default=0, null=True)  # Unix time for the bet
	bet_size = mls.IntegerField(default=0, null=True)  # Size of bet in satoshis
	bet_strike = mls.FloatField(default=0, null=True)
	bet_payout = mls.FloatField(default=0, null=True)
	option_expire = mls.IntegerField(default=0, null=True)
	bet_outcome = mls.CharField(max_length=10, null=True)
	def __unicode__(self):
		return self.user

class AssetPrices(mls.Model):
	time = mls.IntegerField(default=0)
	eurusd = mls.FloatField(default=0, null=True)
	usdjpy = mls.FloatField(default=0, null=True)




# Add Deposit/Funds model
class Deposits(mls.Model):
	username = mls.CharField(max_length=30,null=True)
	time = mls.IntegerField(default=0)
	size = mls.IntegerField(default=0, null=True)  # Size of bet in satoshis
	def __unicode__(self):
		return self.username

class Balances(mls.Model):
	username = mls.CharField(max_length=30,null=True)
	balance = mls.IntegerField(default=0)
	def __unicode__(self):
		return self.username

# Add Last time checked for settled transactions
