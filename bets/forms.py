from django import forms
from bets.models import PlacedBets
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



class BetForm(forms.ModelForm):
	bet_size = forms.FloatField()
	class Meta:
		model = PlacedBets
		fields=('bet_size',)

