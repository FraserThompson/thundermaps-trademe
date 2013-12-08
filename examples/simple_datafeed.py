#!/usr/bin/env python
#
# This example shows how to take data from a simple data feed and post it to ThunderMaps.
# It should be used for a data feed that does not update.
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
	# Add the report to the list of reports.
	reports.append(report)

# If there is at least one report, send the reports to Thundermaps.
if len(reports) > 0:
	# Upload 10 at a time.
	for some_reports in [reports[i:i+10] for i in range(0, len(reports), 10)]:
		tm.sendReports(THUNDERMAPS_ACCOUNT_ID, some_reports)
