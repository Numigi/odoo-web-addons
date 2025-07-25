# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Web Search Date Range",
    "version": "1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add date range filters to the search filters dropdown menu.",
    "depends": [
        "web",
    ],
    "data": [
        "data/search_date_range.xml",
        "views/assets.xml",
        "views/search_date_range.xml",
        "views/search_date_range_filters.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": [
        "static/src/xml/search_filters.xml",
    ],
    "installable": True,
}
