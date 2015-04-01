# Create your views here.a


from bets.forms import UserForm, UserProfileForm, BetForm
from bets.models import PlacedBets, AssetPrices, OfferedOptions
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import OptionTools as tools
reload(tools)

import time
import datetime
import random
import json

def index(request):
    current_user = request.user
    context = RequestContext(request)
    bets_form = BetForm()
    context_dict = {'bets_form': bets_form, 'user':current_user} 
    return render_to_response('bets/index.html', context_dict, context)


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
    return render_to_response(
            'bets/register.html',
            {'user_form': user_form, 'registered': registered},
            context)


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
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('bets/login.html', {}, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/bets/')


# For GET requests (probably not very safe)
def place_bets2(request):
	current_user = request.user
	if not request.user.is_authenticated():
		return HttpResponse("Please Log in")
	
	if request.method == 'GET':
		new_bet = PlacedBets()

		new_bet.bet_time = int(time.time())
	
		new_bet.bet_type = request.GET['bet_type']
		new_bet.bet_size = request.GET['bet_size']
		new_bet.user = current_user.username
		new_bet.bet_payout = 1.5
		new_bet.bet_outcome = "Pending"
		print new_bet.bet_size

		new_bet.save()
		print "here"
		return  HttpResponse("Bet Successful")
	else:
		return HttpResponse(current_user.username)



def place_bets(request):
	if not request.user.is_authenticated():
		return HttpResponse("Please log in")
	current_user = request.user
	if request.method == 'POST':
		bet_form = BetForm(request.POST)
		if bet_form.is_valid():
			new_bet = bet_form.save(commit=False)

			new_bet.bet_time = int(time.time()	)
		
			new_bet.option_asset = request.POST['asset']
			new_bet.bet_strike=request.POST['bet_strike']
			new_bet.bet_type=request.POST['bet_type']
			new_bet.user = current_user.username
			new_bet.bet_payout = request.POST['bet_payout'] 
			new_bet.option_expire = OfferedOptions.objects.latest('open_time').expire_time
			new_bet.bet_outcome = "Pending"
			new_bet.save()
			option_time = datetime.datetime.fromtimestamp(new_bet.bet_time)
			return  HttpResponse("Succesfully purchased a %s option with strike %s and a payout of %s at %s" \
							%(new_bet.bet_type, new_bet.bet_strike, new_bet.bet_payout, str(option_time)))
		else:
			return HttpResponse(bet_form.errors)
	else:
		return HttpResponse(current_user.username)




def update(request):

	last = AssetPrices.objects.latest('time')
	current_option = OfferedOptions.objects.latest('open_time')
	lid = current_option.id

	# Update prices in the OfferedOptions table
	if lid > 1:
		prev_option = OfferedOptions.objects.get(id=lid-1)
		if last.time >= prev_option.expire_time and prev_option.eurusd_close is None:
			prev_option.eurusd_close = tools.get_price(prev_option.expire_time)
			prev_option.save()
			print "Updated Previous Option Close Price ", prev_option.eurusd_close


	# Settle Bets
	if last.time % 300 < 25: # only check in the beginning of the period (efficiency)
		pending = PlacedBets.objects.filter(bet_outcome="Pending")

		for bet in pending:
			eurusd_close = OfferedOptions.objects.get(expire_time=bet.option_expire).eurusd_close
			if eurusd_close is not None:
				if bet.bet_type == "CALL" and eurusd_close > bet.bet_strike:
					bet.bet_outcome = "Success"
				elif bet.bet_type == "CALL" and eurusd_close < bet.bet_strike:
					bet.bet_outcome = "Loss"
				elif bet.bet_type == "PUT" and eurusd_close < bet.bet_strike:
					bet.bet_outcome = "Success"
				elif bet.bet_type == "PUT" and eurusd_close > bet.bet_strike:
					bet.bet_outcome = "Loss"
				else:
					print "Error"
			bet.save()


	# Update remaining prices, payous etc.
	if request.method == 'GET':

		latest_time = str(datetime.datetime.fromtimestamp(last.time))
		asset_price = last.eurusd
		#asset_price = random.normalvariate(last.eurusd, 0.01)
		expire = current_option.expire_time

		call_strike1, call_strike2, call_payout1, call_payout2, \
		put_strike1, put_strike2, put_payout1, put_payout2 = \
				tools.option_params(current_option.open_time, expire, current_option.eurusd_open, last.time, asset_price)
		res = json.dumps({"time":latest_time, "eurusd":round(asset_price,4), 
					"call_strike1":call_strike1, "call_strike2":call_strike2, 
					"expire":str(datetime.datetime.fromtimestamp(expire)), "call_payout1":call_payout1, "call_payout2":call_payout2,
					"put_strike1":put_strike1, "put_strike2":put_strike2, "put_payout1":put_payout1, "put_payout2":put_payout2})
		return HttpResponse(res, mimetype='application/json')
	else:
		return HttpResponse('else')
