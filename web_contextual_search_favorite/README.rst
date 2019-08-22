Web Contextual Search Favorite
==============================
In a list view, when you add a favorite by clicking on Favorites -> Add to my Dashboard,
the saved view is not contextual.

Odoo evaluates the search filters at the moment you click on the button and stores the result in your custom dashboard.
Therefore, if you have a date filter that indiquates today, the view will be stored with an hardcoded string date.
If you go back to this view another day, the view will not be refreshed.

Differences with Odoo version 11.0
----------------------------------
In Odoo version 11.0, we had the same issue when adding a custom filter.
Custom filters were evaluated when clicking on Save.

Building Assets
---------------
If you modify a javascript file of this module, then you might need to rebuild the javascrip assets.

Make sure you have webpack-cli installed.
``
npm install -g webpack-cli
``

In order to rebuild the assets, open a terminal and execute the following commands:

``
cd web_contextual_search_favorite/static
webpack-cli
``

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
