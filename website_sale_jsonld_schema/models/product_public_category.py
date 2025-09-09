# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    google_product_category = fields.Char(
        string="Google Product Category",
        help="The complete Google taxonomy category, for example "
             "'Health & Beauty > Medical Equipment > Medical Training Mannequin'."
    )