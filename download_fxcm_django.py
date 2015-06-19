import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_options.settings')
import urllib2
import time

from bets.models import AssetPrices

url = "http://rates.fxcm.com/RatesXML"




while True:

	time.sleep(1)
	try:
		asset = AssetPrices()
		r = urllib2.urlopen(url)
		timestamp = time.time()
		data = r.read()
		x = data.split('\n')
		asset.time = timestamp
		asset.eurusd = float(x[3].split('Bid')[1].strip('</').strip('>'))
		asset.usdjpy = float(x[11].split('Bid')[1].strip('</').strip('>'))

		asset.usdchf =float(x[27].split('Bid')[1].strip('</').strip('>'))
		asset.eurchf = float(x[35].split('Bid')[1].strip('</').strip('>'))
		asset.spx500 = float(x[347].split('Bid')[1].strip('</').strip('>'))
		asset.ftse100 =float(x[363].split('Bid')[1].strip('</').strip('>'))
		asset.nikkei = float(x[411].split('Bid')[1].strip('</').strip('>'))

		asset.oil = float(x[427].split('Bid')[1].strip('</').strip('>'))
		asset.gold =  float(x[443].split('Bid')[1].strip('</').strip('>'))

	
	
		asset.save()
		print timestamp
	except KeyboardInterrupt:
		raise
	except:
		print "Error"
