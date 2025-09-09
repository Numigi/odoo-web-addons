# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Sale JSON-LD Schema",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "AGPL-3",
    "category": "Website",
    "summary": """Adds a complete and dynamic JSON-LD schema.org script to product pages
        for Google Merchant Center and Rich Results optimization.""",
    "description": """
        This module injects a Product schema.org script in JSON-LD format into the
        Odoo eCommerce product page. It dynamically populates fields like brand,
        GTIN (from UPC), MPN, price, availability, and images (including alternatives)
        to improve SEO and data quality for Google Merchant Center.
    """,
    "depends": ["website_sale", "product_barcode_upc", "product_brand"],
    "data": [
        "views/product_public_category_views.xml",
        "views/product_json_ld.xml",
    ],
    "installable": True,
}