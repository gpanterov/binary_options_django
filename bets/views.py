# Create your views here.a


from bets.forms import UserForm, BetForm
from bets.models import PlacedBets, AssetPrices, Deposits, Balances
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


def index(request):

    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'EURUSD'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def usdjpy(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USDJPY'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def eurchf(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'EURCHF'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)


def usdchf(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USDCHF'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def gold(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'XAUUSD'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def oil(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'USOil'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def spx500(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'SPX500'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def uk100(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'UK100'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)

def jpn225(request):
    if not request.user.is_authenticated():
        current_user = None
    else:
        current_user = request.user
	
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user, 'asset':'JPN225'} 
    return render_to_response('bets/new_index_trading_view_simple.html', context_dict, context)



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
min_bet = 0
max_bet = 0.3
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
				return HttpResponse("Bet exceeds maximum bet size. Please enter an amoung lower than %s" %(max_bet))
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

			return  HttpResponse("Succesfully purchased a %s option with strike %s and a payout of %s at %s" \
							%(new_bet.bet_type, new_bet.bet_strike, new_bet.bet_payout, str(option_time)))
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



def update(request):

	timestamp = int(time.time())


	# Update remaining prices, payous etc.
	if request.method == 'GET':
		
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
			time_of_bet = str(datetime.datetime.fromtimestamp(bet.bet_time))

			expiration = str(datetime.datetime.fromtimestamp(bet.option_expire))
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
	if request.method == "POST" and request.POST['promo_code'] == "panterov":
		current_user = request.user
		timestamp = int(time.time())
		entry = Deposits()
		entry.username = current_user.username
		entry.time = timestamp
		entry.size = 100
		entry.save()
		bal = Balances.objects.get(username = request.user.username)
		bal.balance = bal.balance + entry.size
		bal.save()
		return HttpResponse("Deposit Successful")
	else:
		print "Something went wrong with promo code"

		return HttpResponse("Deposit Not Successful")


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
	context = RequestContext(request)
	balance = Balances.objects.get(username = request.user.username).balance


	if request.method == "POST":
		to_address = request.POST['bitcoin_address']
		amount = request.POST['withdraw_amount']
		withdrawn=True

	return render_to_response('bets/new_withdrawal.html',
	{'withdrawn': withdrawn, 'balance':balance, 'to_address':to_address, 'amount':amount},	context)

