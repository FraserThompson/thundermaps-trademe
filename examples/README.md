Examples
========

These examples show how to deal with three different types of datafeeds and post the data to ThunderMaps.

They all use the `thundermaps` module.

simple_datafeed.py
------------------
This example shows how to take data from a simple data feed and post it to ThunderMaps.
It should be used for a data feed that does not update.

updating_datafeed.py
--------------------
This example shows how to take the newest data from an updating data feed and post it to ThunderMaps.
It should be used for a data feed that provides the ability to specifiy the start date for the data returned.

This is the type of datafeed that is used with TradeMe listings.

updating_datafeed_caching.py
----------------------------
This example shows how to take the newest data from an updating data feed and post it to ThunderMaps, while caching which data has already been posted to ThunderMaps.
It should be used for a data feed that doesn't provide the ability to specifiy the start date for the data returned.
