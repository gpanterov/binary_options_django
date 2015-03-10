from django import forms
from bets.models import PlacedBets, UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

class BetForm(forms.ModelForm):
	bet_size = forms.IntegerField()
	class Meta:
		model = PlacedBets
		fields=('bet_size',)

