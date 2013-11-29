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

class TradeMe:
	# Internal requests object used to perform requests.
	# Is replaced by an OAuth1Session object when authenticated.
	trademe = requests

	# Whether to print debug information.
	debug = False

	# Authenticate with the TradeMe API.
	def authenticate(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
		self.trademe = requests_oauthlib.OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=oauth_token, resource_owner_secret=oauth_secret)

	# Set debug mode.
	def debug(self, on=True):
		self.debug = on

	# Get a list of listings from TradeMe.
	def getListings(self, category_id, limit=25, since=time.time()-86400):
		more = True
		page = None
		count = 0
		listings = []

		# While there are more listings to get, get them.
		while more:
			# Build URL.
			url = "http://api.trademe.co.nz/v1/Search/General.json"
			params = {"category": category_id}
			params["rows"] = 500 if limit == None else limit - count
			if since != None:
				params["date_from"] = datetime.datetime.utcfromtimestamp(since).strftime('%Y-%m-%dT%H:%M:%SZ')
			if page != None:
				params["page"] = page
			# Print debug information in debug mode.
			if self.debug == True:
				print "trademe: [url=%s, params=%s]" % (url, params)
			# Peform the request.
			try:
				resp = self.trademe.get(url, params=params)
				result = resp.json()
			except Exception as e:
				print "Error retrieving listings: %s" % e
				return listings
			# Add each rental to the result.
			for rental in result["List"]:
				listings.append(rental)
				count = count + 1
			# Get next page if there are more listings.
			if (count >= result["TotalCount"]) or (limit != None and count >= limit):
				more = None
			else:
				page = result["Page"] + 1
		return listings
