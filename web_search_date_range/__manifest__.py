# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Web Search Date Range",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add date range filters to the search filters dropdown menu.",
    "depends": [
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/search_date_range.xml",
        "views/search_date_range_views.xml",
        "views/search_date_range_filter_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/web_search_date_range/static/src/js/*",
        ],
    },
    "installable": True,
}
