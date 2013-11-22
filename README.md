Thundermaps-TradeMe
===================

This repository provides Python modules for using the TradeMe API to get property listings, and using the ThunderMaps API to post reports.

Dependencies
------------

* The `requests` and `requests_oauthlib` libraries for Python.
* A Thundermaps API key and account ID.
* *(Optional)* A TradeMe API key, API secret, OAuth token, and OAuth secret.

Usage
-----

### TradeMe module

To use the TradeMe module, import it into your code using `import trademe`.

To get listings for rental properties, you can use the `getRentals()` method:

```python
import trademe

# Get rentals from TradeMe.
rentals = trademe.getRentals(limit=10)
```

If you have a TradeMe developer account and have generated an OAuth token and OAuth secret, then you can authenticate with the TradeMe API prior to making a request in order to increase you rate limit and the number of results you can get per API call. E.g.

```python
import trademe

# Replace ... with the actual values.
TRADEME_API_KEY = "..."
TRADEME_API_SECRET = "..."
TRADEME_OAUTH_KEY = "..."
TRADEME_OAUTH_SECRET = "..."

# Authenticate with TradeMe.
trademe.authenticate(TRADEME_API_KEY, TRADEME_API_SECRET, TRADEME_OAUTH_KEY, TRADEME_OAUTH_SECRET)

# Get rentals from TradeMe.
rentals = trademe.getRentals(limit=10)
```

### Thundermaps module

To use the Thundermaps module, import it into your code using `import thundermaps`. All of the methods in this module require your Thundermaps API key as the first argument. E.g.

```python
import thundermaps

# Replace ... with the actual values.
THUNDERMAPS_API_KEY = "..."
ACCOUNT_ID = ...

# Get reports for an account.
reports = thundermaps.getReports(THUNDERMAPS_API_KEY, ACCOUNT_ID)
```
