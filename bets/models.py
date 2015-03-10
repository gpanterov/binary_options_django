from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	def __unicode__(self):
		return self.user.username


class PlacedBets(models.Model):
	user = models.CharField(max_length=30,null=True)
	bet_time = models.IntegerField(default=0, null=True)  # Unix time for the bet
	bet_size = models.IntegerField(default=0, null=True)  # Size of bet in satoshis
	bet_type = models.CharField(max_length=10,null=True)
	bet_payout = models.FloatField(default=0, null=True)
	bet_outcome = models.CharField(max_length=10, null=True)
	def __unicode__(self):
		return self.user
# Create your models here.
