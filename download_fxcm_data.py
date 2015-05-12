import urllib2
import xmltodict
import time
import datetime

url = "http://rates.fxcm.com/RatesXML"

while True:
	try:

		time.sleep(0.9)
		r = urllib2.urlopen(url)
		data = r.read()
		xml = xmltodict.parse(data)
		timestamp = time.time()
		bid_eurusd = float(xml['Rates']['Rate'][0]['Bid'])
		ask_eurusd = float(xml['Rates']['Rate'][0]['Ask'])

		print datetime.datetime.fromtimestamp(timestamp), '|||||', bid_eurusd, '|||||', ask_eurusd

	except KeyboardInterrupt:
		raise
	except:
		print "Error"
