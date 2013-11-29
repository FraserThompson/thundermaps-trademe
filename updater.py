import thundermaps
import trademe
import time

class Updater:
	categories = {}

	def __init__(self, key):
		self.thundermaps = thundermaps.ThunderMaps(key)
		self.trademe = trademe.TradeMe()

	def authenticate(self, key, secret, oauth_key, oauth_secret):
		self.trademe.authenticate(key, secret, oauth_key, oauth_secret)

	def add_category(self, name, trademe_id, account_id, thundermaps_id):
		# Add the category.
		self.categories[name] = {
			"trademe_id": trademe_id,
			"account_id": account_id,
			"thundermaps_id": thundermaps_id,
			"since": int(time.time())
		}

		# Try to load the last update time from file.
		try:
			update_file = open(".lastupdate_" + name, "r")
			self.categories[name]["since"] = int(update_file.read())
			update_file.close()
		except Exception as e:
			print "* No valid timestamp file was found for '%s': defaulting to now." % name

	# Start updating the categories.
	def start(self):
		# Run until interrupt received.
		while True:
			for category_name in self.categories:
				category = self.categories[category_name]

				# Get listings from TradeMe.
				listings = self.trademe.getListings(category_id=category["trademe_id"], limit=None, since=category["since"])

				# Update timestamp of last update.
				category["since"] = time.time()

				# Create reports for the listings.
				reports = []
				for listing in listings:
					# Some listings don't have geographic information: ignore these.
					if "GeographicLocation" not in listing.keys():
						continue
					# Include the auction URL in the description.
					listing_url = "http://www.trademe.co.nz%s/auction-%d.html" % (listing["CategoryPath"], listing["ListingId"])
					report = {
						"latitude": listing["GeographicLocation"]["Latitude"],
						"longitude": listing["GeographicLocation"]["Longitude"],
						"category_id": category["thundermaps_id"],
						"occurred_on": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(float(listing["StartDate"][6:-2])/1000)),
						"description": "%s. See more at %s" % (("%s - %s" % (listing["Address"], listing["Title"]), listing_url) if "Address" in listing.keys() else (listing["Title"], listing_url)),
						"source_id": "%d" % listing["ListingId"]
					}
					reports.append(report)
				print "Retrieved %d reports for '%s'..." % (len(reports), category_name)

				# If there is at least one report, send the reports to Thundermaps.
				if len(reports) > 0:
					self.thundermaps.sendReports(category["account_id"], reports)
					print "Submitted %d reports..." % len(reports)

				# Save the timestamp of the last update.
				try:
					update_file = open(".lastupdate_" + category_name, "w")
					update_file.write("%d" % category["since"])
					update_file.close()
				except Exception as e:
					print "! WARNING: Unable to write timestamp file for '%s'." % category_name
					print "! If there is an old timestamp file when this script is next run, it may be using an old timestamp resulting in duplicate reports."
					print "! To avoid this, delete the file '.lastupdate_%s'." % category_name

			# Wait half an hour before trying again.
			time.sleep(60 * 30)

