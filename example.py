#!/usr/bin/env python
import thundermaps
import trademe
import time

# Thundermaps account ID and API key.
THUNDERMAPS_API_KEY = "..."
THUNDERMAPS_ACCOUNT_ID = ...

# TradeMe categories.
RENTAL_CATEGORY_ID = 1730

# TradeMe API key for greater rate limiting.
TRADEME_API_KEY = "..."
TRADEME_API_SECRET = "..."
TRADEME_OAUTH_KEY = "..."
TRADEME_OAUTH_SECRET = "..."

# Authenticate with TradeMe.
trademe.authenticate(TRADEME_API_KEY, TRADEME_API_SECRET, TRADEME_OAUTH_KEY, TRADEME_OAUTH_SECRET)

# Start getting listings for one day ago.
since = time.time() - 86400

while True:
	# Get rentals from TradeMe.
	rentals = trademe.getRentals(limit=None, since=since)

	# Update timestamp of last update.
	since = time.time()
	
	# Create reports for the rentals.
	reports = []
	for rental in rentals:
		# Some rentals don't have geographic information: ignore these.
		if "GeographicLocation" not in rental.keys():
			continue
		# Include the auction URL in the description.
		rental_url = "http://www.trademe.co.nz%s/auction-%d.html" % (rental["CategoryPath"], rental["ListingId"])
		report = {
			"latitude": rental["GeographicLocation"]["Latitude"],
			"longitude": rental["GeographicLocation"]["Longitude"],
			"category_id": RENTAL_CATEGORY_ID,
			"cat2": rental["Suburb"],
			"occurred_on": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(float(rental["StartDate"][6:-2])/1000)),
			"description": "%s. See more at %s" % (("%s - %s" % (rental["Address"], rental["Title"]), rental_url) if "Address" in rental.keys() else (rental["Title"], rental_url)),
			"source_id": "%d" % rental["ListingId"]
		}
		reports.append(report)
		print "Retrieved %d reports..." % len(reports)
	
	# If there is at least one report, send the reports to Thundermaps.
	if len(reports) > 0:
		thundermaps.sendReports(THUNDERMAPS_API_KEY, THUNDERMAPS_ACCOUNT_ID, reports)
		print "Submitted %d reports..." % len(reports)

	# Wait half an hour before trying again.
	time.sleep(60 * 30)
