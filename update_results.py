import urllib2
import time
url = "http://gpanterov.pythonanywhere.com/bets/update_results"
url = "http://127.0.0.1:8000/bets/update_results"
while True:
	try:
		time.sleep(0.4)
		if time.time() % 300 <= 3:  # every 5 minutes update
			r = urllib2.urlopen(url)
	except KeyboardInterrupt:
		raise
	except:
		print "Error"
