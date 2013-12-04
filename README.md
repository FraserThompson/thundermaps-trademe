Thundermaps-TradeMe
===================

This repository provides Python modules for using the [TradeMe](http://www.trademe.co.nz/) API to get property listings and using the [ThunderMaps](http://thundermaps.com/) API to post reports, and a module that periodically creates Thundermaps reports for the latest TradeMe listings.

Dependencies
------------

* The `requests` and `requests_oauthlib` libraries for Python.
* A Thundermaps API key and account ID.
* *(Optional)* A TradeMe API key, API secret, OAuth token, and OAuth secret.

Usage
-----

### TradeMe module

To use the TradeMe module, import it into your code using `import trademe` and create an instance of the `TradeMe` class.

To get listings for a certain category, you can use the `getListings` method:

```python
import trademe

# Categories.
TRADEME_CATEGORY_RENTAL = 4233

# Get rentals from TradeMe.
my_trademe = trademe.TradeMe()
listings = my_trademe.getListings(category_id=TRADEME_CATEGORY_RENTAL, limit=10)
```

If you have a TradeMe developer account and have generated an OAuth token and OAuth secret, then you can authenticate with the TradeMe API prior to making a request in order to increase you rate limit and the number of results you can get per API call. E.g.

```python
import trademe

# Replace ... with the actual values.
TRADEME_API_KEY = "..."
TRADEME_API_SECRET = "..."
TRADEME_OAUTH_KEY = "..."
TRADEME_OAUTH_SECRET = "..."

# Categories.
TRADEME_CATEGORY_RENTAL = 4233

# Authenticate with TradeMe.
my_trademe = trademe.TradeMe()
trademe.authenticate(TRADEME_API_KEY, TRADEME_API_SECRET, TRADEME_OAUTH_KEY, TRADEME_OAUTH_SECRET)

# Get rentals from TradeMe.
listings = my_trademe.getListings(category_id=TRADEME_CATEGORY_RENTAL, limit=10)
```

### Thundermaps module

To use the Thundermaps module, import it into your code using `import thundermaps` and create an instance of the `ThunderMaps` class using your Thundermaps API key. E.g.

```python
import thundermaps

# Replace ... with the actual values.
THUNDERMAPS_API_KEY = "..."
ACCOUNT_ID = ...

# Get reports for an account.
my_thundermaps = thundermaps.ThunderMaps(THUNDERMAPS_API_KEY)
reports = thundermaps.getReports(ACCOUNT_ID)
```

### Updater module

The updater module combines both the TradeMe and ThunderMaps module and provides a higher level interface for generating ThunderMaps reports for the latest TradeMe listings.
Using the updater module typically consists of these steps:

* Creating a new instance of `Updater` with a ThunderMaps API key.
* *(Optional)* Authenticating with TradeMe.
* Adding categories to generate reports for.
* Starting the updater.

An example usage is shown below.

```
import updater

# Define categories, keys, and accounts here.

# Create updater and authenticate.
properties_updater = updater.Updater(THUNDERMAPS_API_KEY)
properties_updater.authenticate(TRADEME_API_KEY, TRADEME_API_SECRET, TRADEME_OAUTH_KEY, TRADEME_OAUTH_SECRET)

# Add categories.
properties_updater.add_category("rentals", TRADEME_CATEGORY_RENTAL, THUNDERMAPS_ACCOUNT_RENTALS, THUNDERMAPS_CATEGORY_RENTAL)

# Start updating.
properties_updater.start()
```

**Important:** The updater module uses `.lastupdate_` files to store the timestamp of the last update for each category. If you delete these files then it will default to generating reports from the current time.

## Current Usage

These modules are currently used in several Thundermaps accounts:

* [TradeMe Properties - Rentals](http://app.thundermaps.com/accounts/trademe-properties)
* [TradeMe Properties - For Sale](http://app.thundermaps.com/accounts/trademe-properties-for-sale)
* [TradeMe Properties - Carparks](http://app.thundermaps.com/accounts/trademe-properties-carparks)
* [TradeMe Properties - Flatmates Wanted](http://app.thundermaps.com/accounts/trademe-properties-flatmates-wanted)
