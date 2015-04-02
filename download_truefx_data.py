import time
import bs4
import datetime
import urllib2
import sqlite3 as lite
import random

con = lite.connect('bets.db')
with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM bets_assetprices;")
	data = cur.fetchall()

lid=len(data)
old_residual = 2
while True:
	t = time.time()

	try:
		###########################
		# Download the forex data #
		###########################
		time.sleep(0.75)
		url = 'http://webrates.truefx.com/rates/connect.html?f=html'

		timestamp = int(time.time())
		r = urllib2.urlopen(url)
		data = r.read()
		soup = bs4.BeautifulSoup(data)
		tr = soup.find_all('tr')  # all <tr> tags

		eurusd = tr[0].find_all('td')
		usdchf = tr[4].find_all('td')
		usdjpy = tr[1].find_all('td')
		eurjpy = tr[5].find_all('td')

		#  1.0772        119.9      EUR/USD
		bid_eurusd = eurusd[2].get_text() + eurusd[3].get_text()
		ask_eurusd = eurusd[4].get_text() + eurusd[5].get_text()
		mid_eurusd =float(bid_eurusd) + (float(ask_eurusd) - float(bid_eurusd))/2.
		price_eurusd = round(float(bid_eurusd), 4)

		# USD/CHF
		bid_usdchf = usdchf[2].get_text() + usdchf[3].get_text()
		ask_usdchf = usdchf[4].get_text() + usdchf[5].get_text()
		mid_usdchf =float(bid_usdchf) + (float(ask_usdchf) - float(bid_usdchf))/2.
		price_usdchf = round(float(bid_usdchf), 4)

		# USD/JPY
		bid_usdjpy = usdjpy[2].get_text() + usdjpy[3].get_text()
		ask_usdjpy = usdjpy[4].get_text() + usdjpy[5].get_text()
		mid_usdjpy =float(bid_usdjpy) + (float(ask_usdjpy) - float(bid_usdjpy))/2.
		price_usdjpy = round(float(bid_usdjpy), 2)

		# EUR/JP  1.0772        119.9     Y
		bid_eurjpy = eurjpy[2].get_text() + eurjpy[3].get_text()
		ask_eurjpy = eurjpy[4].get_text() + eurjpy[5].get_text()
		mid_eurjpy =float(bid_eurjpy) + (float(ask_eurjpy) - float(bid_eurjpy))/2.
		price_eurjpy = round(float(bid_eurjpy), 2)

		#################
		# Write to file #
		#price_eurusd += random.randint(1,9) / 10000.
		#price_usdjpy += random.randint(1,9)/100.


		# Attempt to forward fill the database. Leave for now.
#		if lid > 0:
#			with con:
#				cur = con.cursor()
#				cur.execute("SELECT time, eurusd, usdjpy FROM bets_assetprices WHERE Id = %s" % (lid))
#				old_timestamp, _eurusd, _usdjpy = cur.fetchone()
#			for t in range(old_timestamp + 1, timestamp):
#				print "Forward fill ", datetime.datetime.fromtimestamp(t), _eurusd
#				with con:
#					cur = con.cursor()
#					cur.execute("INSERT INTO bets_assetprices(time, eurusd, usdjpy) VALUES (%s, %s, %s);" % (t, _eurusd, _usdjpy))
#
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO bets_assetprices(time, eurusd, usdjpy) VALUES (%s, %s, %s);" % (timestamp, price_eurusd, price_usdjpy))
			lid = cur.lastrowid
			new_residual = timestamp % 300

		print "Time: ", datetime.datetime.fromtimestamp(timestamp), " Price: ", price_eurusd
	except KeyboardInterrupt:
		raise
#	except:
#		print "Error"
