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

Since version 12.0, these are evaluated when rendering the view.
Dashboard are still non-contextual, so this module is still relevant for that part.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
