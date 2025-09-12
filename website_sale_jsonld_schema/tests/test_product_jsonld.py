# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
import json


class TestProductJsonLd(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crée un produit de test
        self.product = self.env['product.template'].create({
            'name': "Test Product",
            'list_price': 99.99,
            'default_code': "SKU123",
            'weight': 1.5,
        })

        self.public_category = self.env['product.public.category'].create({
            'name': "Test Category",
            'google_product_category': "Apparel & Accessories > Shoes",
        })

        self.product.public_categ_ids = [(6, 0, [self.public_category.id])]

    def test_jsonld_escape(self):
        """ Vérifie que les caractères spéciaux sont correctement échappés """
        text = 'Chaussure "spéciale"'
        escaped = self.product.jsonld_escape(text)
        self.assertIn('\\"', escaped)

    def test_get_jsonld_images_with_placeholder(self):
        """ Vérifie que le placeholder est utilisé si pas d'image """
        images = self.product.get_jsonld_images()
        self.assertTrue(any("placeholder" in url for url in images))

    def test_get_jsonld_price_info(self):
        """ Vérifie que le prix est bien renvoyé """
        price_info = self.product.get_jsonld_price_info()
        self.assertEqual(price_info['price'], self.product.list_price)
        self.assertIn('currency', price_info)

    def test_get_jsonld_product_type(self):
        """ Vérifie que le breadcrumb de catégorie est correct """
        product_type = self.product.get_jsonld_product_type()
        self.assertIn("Test Category", product_type)

    def test_get_jsonld_google_product_category(self):
        """ Vérifie que la Google Product Category est bien renvoyée """
        gcat = self.product.get_jsonld_google_product_category()
        self.assertEqual(gcat, "Apparel & Accessories > Shoes")

    def test_render_jsonld_template(self):
        """ Vérifie que le template JSON-LD contient les champs attendus """
        website = self.env['website'].get_current_website()
        rendered = self.env['ir.qweb']._render(
            'website_sale_jsonld_schema.product_json_ld_schema',
            values={'product': self.product, 'website': website},
        )
        # Convertir en dict Python pour vérifier les champs
        data_str = rendered.decode() if isinstance(rendered, bytes) else rendered
        json_str = data_str.split("<script type=\"application/ld+json\">")[1].split(
            "</script>")[0]
        data = json.loads(json_str)

        self.assertEqual(data["@type"], "Product")
        self.assertEqual(data["name"], self.product.name)
        self.assertEqual(data["sku"], self.product.default_code)
        self.assertIn("offers", data)
        self.assertEqual(data["offers"]["availability"], "https://schema.org/InStock")
