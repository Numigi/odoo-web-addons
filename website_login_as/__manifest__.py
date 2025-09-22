# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Login as another user in website",
    "version": "14.0.1.0.1",
    "author": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
Allows to login as another user in website
For example, this option could be useful to check what's displayed
for your customers.

""",
    "depends": ["website"],
    "data": [
        "views/res_users_view.xml",
        "views/webclient_templates.xml",
    ],
    "demo": [],
    "qweb": [
        "static/src/xml/login_as.xml",
    ],
    "installable": True,
}
