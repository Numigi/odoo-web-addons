Web Contextual Search Favorite
==============================

In a list view, when you add a favorite by clicking on Favorites -> Save current search (or Add to my Dashboard),
the saved filters are not contextual.

Odoo evaluates the search filters at the moment you click on the button and stores the result in your custom search filter or dashboard.

This behavior comes with an important limitation.
Filters based on date ranges need to be deleted and recreated every time you need to use them.

This module prevents the evaluation of the domain when the custom filter is saved.
This way, each time you apply your filter, it will be evaulated based on the current day.

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
