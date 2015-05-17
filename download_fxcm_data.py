import urllib2
import xmltodict
import time
import datetime
import sqlite3 as lite


url = "http://rates.fxcm.com/RatesXML"


con = lite.connect('bets.db')
with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM bets_assetprices;")
	data = cur.fetchall()


while True:
	try:

		time.sleep(0.9)
		r = urllib2.urlopen(url)
		data = r.read()
		xml = xmltodict.parse(data)
		timestamp = time.time()
		bid_eurusd = float(xml['Rates']['Rate'][0]['Bid'])
		ask_eurusd = float(xml['Rates']['Rate'][0]['Ask'])
		price_eurusd = bid_eurusd
		price_usdjpy = bid_eurusd

		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO bets_assetprices(time, eurusd, usdjpy) VALUES (%s, %s, %s);" % (timestamp, price_eurusd, price_usdjpy))

		print datetime.datetime.fromtimestamp(timestamp), '|||||', bid_eurusd, '|||||', ask_eurusd

	except KeyboardInterrupt:
		raise
	except:
		
		print "Error"
