# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Sale Carrier Account",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Allow customers to enter their carrier account number at checkout.",
    "depends": ["website_sale", "delivery", "website_sale_delivery"],
    "data": [
        "views/assets.xml",
        "views/delivery_carrier_views.xml",
        "views/website_sale_templates.xml",
    ],
    "installable": True,
}
