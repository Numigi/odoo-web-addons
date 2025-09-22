# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Multi Website User Access",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "AGPL-3",
    "category": "Website",
    "depends": [
        "website",
    ],
    "summary": "Restrict user access to specific websites",
    "data": [
        "views/website_views.xml",
        "views/website_templates.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "post_init_hook": "set_default_website",
}
