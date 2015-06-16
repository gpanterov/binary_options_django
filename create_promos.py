import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_options.settings')
from bets.models import Promos


list_code = ['1ABX123', '67YUZ3', '1DYU34X', '123']
value = 0.3
for code in list_code:
	if len(Promos.objects.filter(code=code)) == 0:  # If this code hasn't been entered in the db
		promo = Promos()
		promo.code = code
		promo.value = value
		promo.save()
	else:
		print "%s has been entered into the db previously" %(code)
