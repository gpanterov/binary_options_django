import sys, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binary_options.settings')
import urllib2
import xmltodict
import time
import datetime

from bets.models import AssetPrices

url = "http://rates.fxcm.com/RatesXML"




while True:
	try:
		asset = AssetPrices()
		time.sleep(0.9)
		r = urllib2.urlopen(url)
		data = r.read()
		xml = xmltodict.parse(data)
		timestamp = time.time()
		asset.time = timestamp
		asset.eurusd = float(xml['Rates']['Rate'][0]['Bid'])
		asset.usdjpy = float(xml['Rates']['Rate'][1]['Bid'])
		asset.usdchf = float(xml['Rates']['Rate'][3]['Bid'])
		asset.eurchf = float(xml['Rates']['Rate'][4]['Bid'])

		asset.spx500 = float(xml['Rates']['Rate'][43]['Bid'])
		asset.ftse100 = float(xml['Rates']['Rate'][45]['Bid'])
		asset.nikkei = float(xml['Rates']['Rate'][51]['Bid'])


		asset.oil = float(xml['Rates']['Rate'][53]['Bid'])
		asset.gold =  float(xml['Rates']['Rate'][55]['Bid'])


		asset.save()

	except KeyboardInterrupt:
		raise
	except:
		
		print "Error"
