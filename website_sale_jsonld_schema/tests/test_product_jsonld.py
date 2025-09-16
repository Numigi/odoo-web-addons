# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo.tests.common import TransactionCase


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

    def test_get_jsonld_schema_basic_structure(self):
        """Test that the JSON-LD schema has the correct basic structure."""
        json_str = self.product._get_jsonld_schema()
        data = json.loads(json_str)
        
        self.assertEqual(data["@context"], "https://schema.org/")
        self.assertEqual(data["@type"], "Product")
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["sku"], "SKU123")

    def test_get_jsonld_schema_with_category(self):
        """Test that categories are properly included in the schema."""
        json_str = self.product._get_jsonld_schema()
        data = json.loads(json_str)
        
        self.assertIn("category", data)
        self.assertEqual(data["category"], "Test Category")
        self.assertIn("google_product_category", data)
        self.assertEqual(data["google_product_category"], "Apparel & Accessories > Shoes")

    def test_get_jsonld_schema_offers_structure(self):
        """Test that offers section is properly structured."""
        json_str = self.product._get_jsonld_schema()
        data = json.loads(json_str)
        
        self.assertIn("offers", data)
        offers = data["offers"]
        self.assertEqual(offers["@type"], "Offer")
        self.assertEqual(offers["itemCondition"], "https://schema.org/NewCondition")
        self.assertEqual(offers["availability"], "https://schema.org/InStock")
        self.assertIn("price", offers)
        self.assertIn("priceCurrency", offers)

    def test_get_jsonld_schema_with_weight(self):
        """Test that shipping weight is included when product has weight."""
        json_str = self.product._get_jsonld_schema()
        data = json.loads(json_str)
        
        self.assertIn("shippingWeight", data)
        weight = data["shippingWeight"]
        self.assertEqual(weight["@type"], "QuantitativeValue")
        self.assertEqual(weight["value"], 1.5)
        self.assertEqual(weight["unitCode"], "KGM")

    def test_get_jsonld_schema_images_fallback(self):
        """Test that placeholder image is used when no product images exist."""
        json_str = self.product._get_jsonld_schema()
        data = json.loads(json_str)
        
        self.assertIn("image", data)
        self.assertTrue(isinstance(data["image"], list))
        self.assertTrue(any("placeholder" in url for url in data["image"]))

    def test_get_jsonld_schema_special_characters(self):
        """Test that special characters are properly escaped in JSON output."""
        self.product.name = 'Chaussure "spéciale" & élégante'
        json_str = self.product._get_jsonld_schema()
        
        # Should not raise JSON decode error
        data = json.loads(json_str)
        self.assertEqual(data["name"], 'Chaussure "spéciale" & élégante')
