#!/usr/bin/env python
#
# This example shows how to take the newest data from an updating data feed and post it to ThunderMaps.
# It should be used for a data feed that provides the ability to specifiy the start date for the data returned.
#
import thundermaps
import time

# Replace ... with your API key.
THUNDERMAPS_API_KEY = "..."

# Replace ... with your account ID and category ID respectively.
THUNDERMAPS_ACCOUNT_ID = ...
THUNDERMAPS_CATEGORY_ID = ...

# Create an instance of the ThunderMaps class.
tm = thundermaps.ThunderMaps(THUNDERMAPS_API_KEY)

# When data was last retrieved. Initially empty so all data can be retrieved.
# For data feeds with lots of data this should initially be set to time.time().
last_updated = None

# Try to load the last update time from file.
try:
	update_file = open(".lastupdate_sample", "r")
	last_updated = int(update_file.read())
	update_file.close()
except Exception as e:
	print "* No valid timestamp file was found. Defaulting to never."


# Run until interrupt received.
while True:
	# Load the data from the data feed that has been added since data was last retrieved.
	# This method should return a list of dicts.
	items = getDataFeed(..., last_updated)

	# Update timestamp of last update.
	last_updated = time.time()

	# Create reports for the listings.
	reports = []
	for item in items:
		# Create the report, filling in the fields using fields from the item data.
		report = {
			"latitude": item["latitude"];
			"longitude": item["longitude"],
			"category_id": THUNDERMAPS_CATEGORY_ID,
			"occurred_on": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(item["time"])),
			"description": item["description"],
			"source_id": item["id"]
		}
		# Add the report to the list of reports.
		reports.append(report)

	# If there is at least one report, send the reports to Thundermaps.
	if len(reports) > 0:
		# Upload 10 at a time.
		for some_reports in [reports[i:i+10] for i in range(0, len(reports), 10)]:
			tm.sendReports(THUNDERMAPS_ACCOUNT_ID, some_reports)

	# Save the timestamp of the last update.
	try:
		update_file = open(".lastupdate_sample", "w")
		update_file.write("%d" % last_updated)
		update_file.close()
	except Exception as e:
		print "! WARNING: Unable to write timestamp file."
		print "! If there is an old timestamp file when this script is next run, it may be using an old timestamp resulting in duplicate reports."
		print "! To avoid this, delete the file '.lastupdate_sample'"

	# Wait half an hour before trying again.
	time.sleep(60 * 30)
