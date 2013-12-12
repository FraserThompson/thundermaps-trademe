#!/usr/bin/env python
#
# This example shows how to take the newest data from an updating data feed and post it to ThunderMaps,
# while caching which data has already been posted to ThunderMaps.
# It should be used for a data feed that doesn't provide the ability to specifiy the start date for the data returned.
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

# Try to load the source_ids already posted.
source_ids = []
try:
	source_ids_file = open(".source_ids_sample", "r")
	source_ids = [i.strip() for i in source_ids_file.readlines()]
	source_ids_file.close()
except Exception as e:
	print "! WARNING: No valid cache file was found. This may cause duplicate reports."

# Run until interrupt received.
while True:
	# Load the data from the data feed.
	# This method should return a list of dicts.
	items = getDataFeed(...)

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
		# Add the report to the list of reports if it hasn't already been posted.
		if report["source_id"] not in source_ids:
			reports.append(report)
		# Add the source id to the list.
		source_ids.append(report["source_id"])

	# If there is at least one report, send the reports to Thundermaps.
	if len(reports) > 0:
		# Upload 10 at a time.
		for some_reports in [reports[i:i+10] for i in range(0, len(reports), 10)]:
			tm.sendReports(THUNDERMAPS_ACCOUNT_ID, some_reports)

	# Save the posted source_ids.
	try:
		source_ids_file = open(".source_ids_sample", "w")
		for i in source_ids:
			source_ids_file.write("%s\n" % i)
		source_ids_file.close()
	except Exception as e:
		print "! WARNING: Unable to write cache file."
		print "! If there is an old cache file when this script is next run, it may result in duplicate reports."

	# Wait half an hour before trying again.
	time.sleep(60 * 30)
