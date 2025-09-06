# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def jsonld_escape(self, text):
        """Escape text for safe inclusion in JSON-LD."""
        if not text:
            return ""
        return json.dumps(str(text))[1:-1]  # Remove outer quotes

    def get_jsonld_images(self):
        """Get list of product images for JSON-LD schema."""
        images = []
        
        # Main product image
        if self.image_1920:
            main_image = self.env['website'].get_current_website().image_url(self, 'image_1920')
            images.append(main_image)
        
        # Additional images
        for image in self.product_template_image_ids:
            if image.image_1920:
                img_url = self.env['website'].get_current_website().image_url(image, 'image_1920')
                images.append(img_url)
        
        # Fallback if no images
        if not images:
            images.append('/web/static/src/img/placeholder.png')
            
        return images

    def get_jsonld_price_info(self):
        """Get price information for current context (pricelist, currency)."""
        website = self.env['website'].get_current_website()
        pricelist = website.get_current_pricelist()
        
        # Get price with current pricelist
        product_context = dict(self.env.context, pricelist=pricelist.id)
        product_with_context = self.with_context(product_context)
        
        price_info = {
            'price': product_with_context.list_price,
            'currency': pricelist.currency_id.name,
            'pricelist': pricelist.id
        }
        
        return price_info

    def get_jsonld_product_type(self):
        """Get product type from first public category in breadcrumb format."""
        if not self.public_categ_ids:
            return ""
        
        # Get first public category
        first_category = self.public_categ_ids[0]
        
        # Get display_name and replace ' / ' with ' > '
        category_path = first_category.display_name.replace(' / ', ' > ')
        
        return category_path

    def get_jsonld_google_product_category(self):
        """Get the Google Product Category from the product's first public category."""
        if not self.public_categ_ids:
            return ""
        
        first_category = self.public_categ_ids[0]
        if first_category.google_product_category:
            return first_category.google_product_category
        
        return ""