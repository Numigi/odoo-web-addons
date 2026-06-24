# Copyright 2026-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# pylint: disable=pointless-statement
# noqa: B018

{
    "name": "Database Name Display",
    "version": "18.0.1.1.0",
    "author": "Interne",
    "category": "Hidden",
    "summary": "Displays the database name in the header (systray) without debug mode.",
    "description": """
         Allows displaying the current database name in the top menu.
        Alternative 2: OWL component reading session.db.
    """,
    "depends": ["web"],
    "data": [
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "web_db_name_display/static/src/db_name_systray.js",
            "web_db_name_display/static/src/db_name_systray.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
