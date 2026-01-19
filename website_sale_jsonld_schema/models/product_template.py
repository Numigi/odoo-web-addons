# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_jsonld_schema(self):
        """
        Build the complete JSON-LD schema as a Python dictionary
        and return it as a JSON string.
        This centralizes all logic and lets json.dumps handle syntax.
        """
        self.ensure_one()
        website = self.env['website'].get_current_website()
        current_lang = self.env.context.get('lang', 'en_US')
        localized_product = self.with_context(lang=current_lang)
        pricelist = website.get_current_pricelist()
        price = self.with_context(pricelist=pricelist.id).price

        # --- Build the schema dictionary ---
        schema = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": localized_product.name,
        }

        # --- Add fields conditionally ---
        if localized_product.description_sale:
            schema["description"] = localized_product.description_sale

        if self.public_categ_ids:
            first_category = self.public_categ_ids[0]
            schema["category"] = first_category.name
            if first_category.google_product_category:
                schema["google_product_category"] = first_category.google_product_category

        if self.default_code:
            schema["sku"] = self.default_code

        if self.product_brand_id and self.product_brand_id.name:
            schema["brand"] = {
                "@type": "Brand",
                "name": self.product_brand_id.with_context(lang=current_lang).name
            }

        # Identifier hierarchy
        if self.upc:
            schema["gtin"] = self.upc
        elif self.manufacturer_pref:
            schema["mpn"] = self.manufacturer_pref

        # Image list
        images = []
        if self.image_1920:
            images.append(website.image_url(self, 'image_1920'))
        for img in self.product_template_image_ids:
            if img.image_1920:
                images.append(website.image_url(img, 'image_1920'))

        if not images:
            images.append(f"{website.get_base_url()}/web/static/src/img/placeholder.png")

        schema["image"] = images

        if self.weight > 0:
            schema["shippingWeight"] = {
                "@type": "QuantitativeValue",
                "value": self.weight,
                "unitCode": "KGM"
            }

        # Offers
        offer_data = {
            "@type": "Offer",
            "url": f"{website.get_base_url()}{localized_product.website_url}",
            "priceCurrency": pricelist.currency_id.name,
            "price": price,
            "itemCondition": "https://schema.org/NewCondition",
            "availability": "https://schema.org/InStock"  # As per your business rule
        }

        if website.company_id.country_id:
            offer_data["areaServed"] = {
                "@type": "Country",
                "name": website.company_id.country_id.name
            }

        schema["offers"] = offer_data

        # Use json.dumps to handle all escaping and comma syntax correctly.
        # ensure_ascii=False is important for names with accents.
        return json.dumps(schema, ensure_ascii=False)
