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

	def add_category(self, name, trademe_id, account_id, thundermaps_id, trademe_api_path="General"):
		# Add the category.
		self.categories[name] = {
			"trademe_id": trademe_id,
			"account_id": account_id,
			"thundermaps_id": thundermaps_id,
			"since": int(time.time()),
			"trademe_api_path": trademe_api_path,
			"previous": []
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
				listings = self.trademe.getListings(category_id=category["trademe_id"], limit=None, since=category["since"], api_path=category["trademe_api_path"])

				# Update timestamp of last update.
				category["since"] = time.time()

				# Create a new "previous" list of listing IDs.
				new_previous = []

				# Create reports for the listings.
				reports = []
				for listing in listings:
					# Some listings don't have geographic information: ignore these.
					if "GeographicLocation" not in listing.keys():
						continue

					# Some listings don't have any accuracy in the location: ignore these.
					if listing["GeographicLocation"]["Accuracy"] == "0":
						continue

					# If the listing was added in the previous iteration, ignore it.
					if listing["ListingId"] in category["previous"]:
						continue

					# Include the auction URL in the description.
					listing_url = "http://www.trademe.co.nz%s/auction-%d.html" % (listing["CategoryPath"], listing["ListingId"])

					# Create base report.
					report = {
						"latitude": listing["GeographicLocation"]["Latitude"],
						"longitude": listing["GeographicLocation"]["Longitude"],
						"category_id": category["thundermaps_id"],
						"occurred_on": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(float(listing["StartDate"][6:-2])/1000)),
						"description": "%s. See more at %s" % (listing["Title"], listing_url),
						"source_id": "%d" % listing["ListingId"]
					}

					# Add as much address information as available.
					address_parts = []
					if "Address" in listing.keys():
						address_parts.append(listing["Address"])
					if "Suburb" in listing.keys():
						address_parts.append(listing["Suburb"])
					if "District" in listing.keys():
						address_parts.append(listing["District"])
					if len(address_parts) > 0:
						address_parts.append("New Zealand")
						report["address"] = ", ".join(address_parts)

					# Add the report to the list of reports.
					reports.append(report)

					# Add the listing ID to the "previous" list.
					new_previous.append(listing["ListingId"])

				print "Retrieved %d reports for '%s'..." % (len(reports), category_name)

				# Update the "previous" list.
				category["previous"] = new_previous

				# If there is at least one report, send the reports to Thundermaps.
				if len(reports) > 0:
					# Upload 10 at a time.
					for some_reports in [reports[i:i+10] for i in range(0, len(reports), 10)]:
						self.thundermaps.sendReports(category["account_id"], some_reports)
						print "Submitted %d reports..." % len(some_reports)

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

