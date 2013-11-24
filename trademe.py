#
# trademe.py
#
# Module for interacting with the TradeMe API.
# In order to have a higher rate limit and be able to access larger amount of
# listings at a time you must known your TradeMe Developer key and secret.
#
# Author: Daniel Gibbs <danielgibbs.name>
#

import requests
import requests_oauthlib
import json
import time
import datetime

# Internal requests object used to perform requests.
# Is replaced by an OAuth1Session object when authenticated.
trademe = requests

# TradeMe category numbers.
RENTAL_CATEGORY = 4233

# Authenticate with the TradeMe API.
def authenticate(consumer_key, consumer_secret, oauth_token, oauth_secret):
	global trademe
	trademe = requests_oauthlib.OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=oauth_token, resource_owner_secret=oauth_secret)

# Unauthenticate from the TradeMe API.
def unauthenticate():
	global trademe
	trademe = requests


# Get a list of rentals from TradeMe.
def getRentals(limit=25, since=time.time()-86400):
	global trademe
	more = True
	page = None
	count = 0
	rentals = []

	# While there are more listings to get, get them.
	while more:	
		# Connect to TradeMe and get a list of rentals.
		url = "http://api.trademe.co.nz/v1/Search/General.json?category=%d" % RENTAL_CATEGORY
		if limit == None:
			url = url + "&rows=500"
		else:
			url = url + "&rows=%d" % (limit - count)
		if since != None:
			url = url + "&date_from=%s" % datetime.datetime.fromtimestamp(since).strftime('%Y-%m-%dT%H:%M:%SZ')
		if page != None:
			url = url + "&page=%d" % page
		try:
			resp = trademe.get(url)
			result = resp.json()
		except Exception as e:
			print "Error retrieving rentals: %s" % e
			return rentals
		# Add each rental to the result.
		for rental in result["List"]:
			rentals.append(rental)
			count = count + 1
		# Get next page if there are more listings.
		if (count >= result["TotalCount"]) or (limit != None and count >= limit):
			more = None
		else:
			page = result["Page"] + 1
	return rentals
