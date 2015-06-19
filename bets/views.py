# Create your views here.a


from bets.forms import UserForm, BetForm
from bets.models import PlacedBets, AssetPrices, Deposits, Balances, Promos
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

import OptionTools as tools
reload(tools)

import time
import datetime
import random
import json
import urllib2, urllib

##############
# Parameters #
##############

min_bet = 0
max_bet = 0.3
my_timezone_offset = 300

def index(request):

    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'EURUSD'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)



def usdjpy(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USDJPY'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)



def eurchf(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'EURCHF'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)




def usdchf(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USDCHF'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)




def gold(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'XAUUSD'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)



def oil(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USOil'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)




def spx500(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'SPX500'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)




def uk100(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'UK100'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)




def jpn225(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'JPN225'} 
    return render_to_response('bets/new_index_trading_view_custom.html', context_dict, context)
















def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False
	password = None
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		# If the two forms are valid...
		if user_form.is_valid():
		# Save the user's form data to the database.

			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			

			# Update our variable to tell the template registration was successful.
			registered = True
			# Create entry for the user's balance
			bal = Balances()
			bal.username = user.username
			bal.balance = 0
			bal.save()

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()

	# Render the template depending on the context.
	return render_to_response('bets/new_register.html',
	{'registered': registered},	context)















def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/bets/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('bets/new_login.html', {}, context)









@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/bets/')











# Must modify the payouts -- should be recalculated every time. Not taken from the html (possible fraud)
def place_bets(request):
	if not request.user.is_authenticated():
		return HttpResponse("Please log in")

	current_user = request.user
	timestamp = int(time.time()	)
	expire = timestamp + 300 - (timestamp % 300)
	if expire - timestamp < 30:
		return  HttpResponse("No Bets 30 seconds prior to expiration")
	if request.method == 'POST':
		try:
			bet_size_float = float(request.POST['bet_size'].strip())
		except:
			return HttpResponse("Please enter a correct amount")


		bet_form = BetForm(request.POST)
		if bet_form.is_valid():
			if bet_size_float > max_bet:
				return HttpResponse("Bet exceeds maximum bet size. Please enter an amount lower than %s" %(max_bet))
			if bet_size_float < min_bet:
				return HttpResponse("Bet size is too low. Please enter an amount greater than %s" %(min_bet))

			option_asset = request.POST['asset']
			latest_price, latest_available_time = tools.get_closest_prices(option_asset, timestamp)
			if timestamp - latest_available_time > 10:
				print "Error - No price data. The latest data is more than 10 seconds older than the current time"
				return HttpResponse("We are currently unable to accept bets. Please try again later")


			bal = Balances.objects.get(username = current_user.username)
			if bet_size_float > bal.balance:
				return HttpResponse("The amount exceeds the available funds in your account")




			new_bet = bet_form.save(commit=False)
			new_bet.bet_time = timestamp		
			new_bet.option_asset = option_asset

			new_bet.bet_strike = latest_price

			new_bet.bet_type=request.POST['bet_type']
			new_bet.user = current_user.username
			new_bet.bet_payout = 1.90

			new_bet.option_expire =  expire
			new_bet.bet_outcome = "Pending"
			new_bet.save()
			option_time = datetime.datetime.fromtimestamp(new_bet.bet_time)

			# Update the balance of the trader
			bal.balance = bal.balance - new_bet.bet_size
			bal.save()

			return  HttpResponse("Succesfully purchased a %s option with strike %s and a payout of %s" \
							%(new_bet.bet_type, new_bet.bet_strike, new_bet.bet_payout))
		else:
			return HttpResponse(bet_form.errors)
	else:
		return HttpResponse(current_user.username)












def update_results(request):
	if request.method == "GET":
		pending = PlacedBets.objects.filter(bet_outcome="Pending")
		all_results = ""
		for bet in pending:
			outcome, price_at_expiration= tools.get_bet_outcome(bet)
			bet.bet_outcome = outcome
			bet.price_at_expiration = price_at_expiration
			bet.save()

			# Update Funds
			if bet.bet_outcome == "Success":
				profit = bet.bet_size * bet.bet_payout
				# Update the balance of the trader
				bal = Balances.objects.get(username = bet.user)
				bal.balance = bal.balance + profit
				bal.save()
			all_results += "<h3>User: %s, Type: %s, Outcome: %s </h3>" %(bet.user, bet.bet_type, bet.bet_outcome)
		
	return HttpResponse(all_results)












def update_quote_custom(request):

	timestamp = time.time()
	current_user = request.user
	try:
		option_asset = request.GET['asset']

		option_type = request.GET['option_type_c'].lower()
		expiration = float(request.GET['expiration_c']) * 60
		strike = float(request.GET['strike_price_c'])
		amount = float(request.GET['amount_c'])
	except:
		return HttpResponse("Error with form. Please enter correct values for expiration, strike and amount")

	# Calculate Option Payout
	latest_price, latest_available_time = tools.get_closest_prices(option_asset, timestamp)
	vol = tools.calculate_asset_vol(option_asset)
	payout = tools.calculate_option_payout(latest_price, strike, expiration, vol, option_type)
	print "Quote Requested"
	print "Latest price: %s, Strike: %s, Volatility: %s, Expiration (seconds): %s, Payout: %s" \
													% (latest_price, strike, vol, expiration, payout)
	bal = Balances.objects.get(username = current_user.username)
	if request.method=="GET":
		payout_pct = int(round((payout - 1) * 100, 0))
		payout_amount = round((1 + payout_pct/100.) * amount, 4)
		res = json.dumps({"payout":payout_pct, "payout_amount":payout_amount})
		return HttpResponse(res, mimetype='application/json')









def place_custom_bet(request):
	timestamp = time.time()
	current_user = request.user
	try:
		option_asset = request.POST['asset']

		option_type = request.POST['option_type_c'].lower()
		expiration = timestamp + float(request.POST['expiration_c']) * 60
		strike = float(request.POST['strike_price_c'])
		amount = float(request.POST['amount_c'])
	except:
		
		return HttpResponse("Error with form. Please enter correct values for expiration, strike and amount")

	# Calculate Option Payout
	latest_price, latest_available_time = tools.get_closest_prices(option_asset, timestamp)
	vol = tools.calculate_asset_vol(option_asset)
	remaining_time = expiration - timestamp
	payout = tools.calculate_option_payout(latest_price, strike, remaining_time, vol, option_type)
	bal = Balances.objects.get(username = current_user.username)

	if request.method=="POST":
		if expiration - timestamp < 30:
			return  HttpResponse("Select time to expiration longer than 30 seconds. No option purchased.")

		if amount < min_bet or amount >max_bet:
			return HttpResponse("Please select amount which is between %s and %s" %(min_bet, max_bet))
		if amount > bal.balance:
				return HttpResponse("The amount exceeds the available funds in your account")

		if timestamp - latest_available_time > 10:
			print "Error - No price data. The latest data is more than 10 seconds older than the current time"
			return HttpResponse("We are currently unable to accept bets. Please try again later")

		shown_payout = request.POST['shown_payout']
		payout_pct = int(round((payout - 1) * 100, 0))


		# If there was a big market move, prompt the user to update again. Otherwise give him the payout that was shown to him.
		print "The current price is %s || The payout seen by the user is: %s ||| The current payout is: %s " % (latest_price, shown_payout, payout_pct)
		if (int(shown_payout) - int(payout_pct)) / float(shown_payout) > 0.025:
			return HttpResponse("The market has moved! The quoted price is no longer accurate. Please update the quote and purchase again")
		else:
			payout_pct = int(shown_payout)

		payout_rounded = (1 + payout_pct/100.)



		new_bet = PlacedBets()
		new_bet.bet_time = timestamp		
		new_bet.option_asset = option_asset
		new_bet.bet_size = amount
		new_bet.bet_strike = strike

		new_bet.bet_type=option_type.upper()
		new_bet.user = current_user.username

		new_bet.bet_payout = payout_rounded

		new_bet.option_expire =  expiration

		new_bet.bet_outcome = "Pending"
		new_bet.save()
		option_time = datetime.datetime.fromtimestamp(new_bet.bet_time)

		# Update the balance of the trader
		bal.balance = bal.balance - new_bet.bet_size
		bal.save()
		print "Placing a Custom Bet"
		print "Latest price: %s, Strike: %s, Volatility: %s, Expiration (seconds): %s, Payout: %s" \
													% (latest_price, strike, vol, remaining_time, payout_rounded)


		option_time = datetime.datetime.fromtimestamp(new_bet.bet_time)
		return  HttpResponse("Succesfully purchased the following option: \nType: %s \nStrike: %s \nPayout: %s " \
								%(new_bet.bet_type, new_bet.bet_strike, new_bet.bet_payout))


def update(request):

	timestamp = int(time.time())


	# Update remaining prices, payous etc.
	if request.method == 'GET':
		user_timezone_offset= int(request.GET['offset'])
		balance = Balances.objects.get(username = request.user.username).balance
		balance = round(balance, 4)
		# Get the last 10 bets of the trader and return them for a table in the website
		recent_bets = PlacedBets.objects.filter(user = request.user.username)
		if len(recent_bets) > 10:
			recent_bets = recent_bets[len(recent_bets) - 10:]
		
		tb = ""
		for bet in recent_bets[::-1]:
			size = bet.bet_size
			if bet.bet_type == "CALL":
				ttype = "<span class = 'badge badge-primary'>Call</span>"
			else:
				ttype = "<span class = 'badge badge-danger'>Put</span>"
			payout = bet.bet_payout
			strike = round(bet.bet_strike,4)
			offset = (my_timezone_offset - user_timezone_offset) * 60
			time_of_bet = str(datetime.datetime.fromtimestamp(bet.bet_time + offset))

			expiration = str(datetime.datetime.fromtimestamp(bet.option_expire + offset))
			outcome = bet.bet_outcome
			price_at_exp = round(bet.price_at_expiration,4)
			if price_at_exp == 0:
				price_at_exp = "N/A"
			tb += "<tr><td>%s</td><td>%s</td><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td><td>%s</td></tr>" % \
							(ttype,time_of_bet, bet.option_asset, size, payout, strike, expiration, price_at_exp, outcome)  



		res = json.dumps({"balance":balance, "tb":tb})
		return HttpResponse(res, mimetype='application/json')
	else:
		return HttpResponse('Not a GET request')


@login_required
def promo(request):
	if request.method == "POST":

		context = RequestContext(request)
		current_user = request.user
		timestamp = int(time.time())

		promo_code = request.POST['promo_code']
		code_db = Promos.objects.filter(code=promo_code)
		promo_successful = False
		if len(code_db)==1 and not code_db[0].used:
			bal = Balances.objects.get(username = request.user.username)
			bal.balance = bal.balance + code_db[0].value
			bal.save()
			code_db[0].used = True
			code_db[0].user = request.user.username
			code_db[0].save()
			promo_successful = True
		else:
			print "Promo code is invalid"


		return render_to_response('bets/new_promos.html',
		{'promo_successful': promo_successful, 'user':current_user.username, 'amount':code_db[0].value},	context)

	else:
		print "Something went wrong with promo code"

		return HttpResponse("Error. Please go back!")


@login_required
def deposit2(request):
	context = RequestContext(request)
	current_user = request.user

	print request.body
	callback_url = "http://gpanterov.pythonanywhere.com/bets/deposit_received/parameters?secret=gogo&user=%s" % (current_user.username,)
	my_wallet = "14AP4q8dGd3wJiuHoRqmirqctaBHjoP6GA"
	input_url = "https://blockchain.info/api/receive?method=create&format=plain&address=%s&shared=false&callback=%s" %(my_wallet, urllib.quote_plus(callback_url))
	r = urllib2.urlopen(input_url)
	Resp = json.loads(r.read())
	
	return render_to_response('bets/new_deposit.html', {'address':Resp['input_address'], 'user':current_user}, context)


def deposit_received(request):
	if request.method == "GET":
		if request.GET['secret'] == "gogo":
			print "secret verified"
			current_user = request.GET['user']
			confirmations = int(request.GET['confirmations'])
			transaction_hash = request.GET['input_transaction_hash']
			input_address = request.GET['input_address']
			timestamp = int(time.time())
			if confirmations >=5:
				return HttpResponse("*OK*")  # Wait for 5 confirmations

			try:
				entry=Deposits.objects.filter(transaction_hash = transaction_hash)[0]
				entry.confirmations = confirmations
				print "Selected old entry"
			except:
				entry = Deposits()
				entry.username = current_user
				entry.time = timestamp
				entry.size = int(request.GET['value']) / 1e8
				entry.transaction_hash = transaction_hash
				entry.input_address = input_address
				entry.confirmations = confirmations
				print "Created a new deposit entry"


			if not entry.included:
				bal = Balances.objects.get(username = str(current_user))
				bal.balance = bal.balance + entry.size
				bal.save()
				entry.included = True
				print "Counted the deposit"

			entry.save()


			return HttpResponse("Deposit Received with %s confirmations" %(confirmations))
		else:
			print "Someone trying to hack you"
	else:
		print "Something went wrong with promo code"

		return HttpResponse("Deposit Not Successful")




@login_required
def withdraw(request):
	withdrawn = False
	to_address = ""
	amount = ""
	form_valid = True
	context = RequestContext(request)

	current_user = request.user.username
	bal = Balances.objects.get(username = str(current_user))
	balance = bal.balance

	if request.method == "POST":
		to_address = request.POST['bitcoin_address']
		amount = request.POST['withdraw_amount']
		try:
			amount_float = float(amount)
			if amount_float > bal.balance:
				form_valid = False
				withdrawn=False

		except:
			form_valid = False
			withdrawn=False
			print "Invalid withdrawal amount"

		if not form_valid:
			print "No money was sent. Exiting. Form was invalid"
			return render_to_response('bets/new_withdrawal.html',
				{'withdrawn': withdrawn, 'balance':balance, 'to_address':to_address, 
								'amount':amount, 'form_valid':form_valid},	context)
		amount = str(int(amount_float * 1e8))
		bal.balance -= float(amount) / 1e8
		balance = bal.balance
		bal.save()

		#r=tools.send_money(to_address, amount)
		#print "Sent %s bitcoins to %s. Output from blockchain: %s" %(amount, to_address , r.read())
		withdrawn=True

	return render_to_response('bets/new_withdrawal.html',
	{'withdrawn': withdrawn, 'balance':balance, 'to_address':to_address, 'amount':amount, 'form_valid':form_valid},	context)

