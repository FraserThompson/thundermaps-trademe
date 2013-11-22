#
# thundermaps.py
#
# Module for interacting with the Thundermaps API.
# To use this you must have registered a Thundermaps and known your API key and account ID.
#
# Author: Daniel Gibbs <danielgibbs.name>
#

import requests
import json

# Send a list of reports to ThunderMaps.
def sendReports(key, account_id, reports):
	try:
		data = json.dumps({"reports": reports})
		url = "http://app.thundermaps.com/api/reports/?account_id=%d&key=%s" % (account_id, key)
		headers = {"Content-Type": "application/json"}
		resp = requests.post(url, data=data, headers=headers)
		return resp
	except Exception as e:
		print "Error creating reports: %s" % e
		return None

# Get a list of reports from ThunderMaps.
def getReports(key, account_id):
	try:
		url = "http://app.thundermaps.com/api/reports/?account_id=%d&key=%s" % (account_id, key)
		resp = requests.get(url)
		result = resp.json()
		return result
	except Exception as e:
		print "Error getting reports: %s" % e
		return None

# Delete a specific report from ThunderMaps.
def deleteReport(key, report_id):
	try:
		url = "http://app.thundermaps.com/api/reports/%d/?key=%s" % (report_id, key)
		resp = requests.delete(url)
		return resp
	except Exception as e:
		print "Error deleting report %d: %s" % (id, e)
		return None
