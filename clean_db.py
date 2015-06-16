"""
Keep the database clean and lean
"""

import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_options.settings')
from bets.models import AssetPrices

Nrecent = 500
output_fname = '../data/price_data'



f = open(output_fname, 'a')
latest_time = AssetPrices.objects.latest('time').time
prices_for_deletion = AssetPrices.objects.filter(time__lte = latest_time - Nrecent)

for entry in prices_for_deletion:
	print entry.id
	line = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \n" % (entry.time, entry.eurusd, 
								entry.usdjpy, entry.usdchf, entry.eurchf, 
								entry.oil, entry.gold, entry.spx500, entry.ftse100, entry.nikkei)
	f.write(line)  # write the discarded data to a file

f.close()

#AssetPrices.objects.filter(time__lte = latest_time - Nrecent).delete()
prices_for_deletion.delete()
