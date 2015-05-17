from django.db import models
from django.contrib.auth.models import User
# went back a commit c34222a2050b9d1f1e8b995de3058cd1ad0d4ddf
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	def __unicode__(self):
		return self.user.username


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

# Add Last time checked for settled transactions
