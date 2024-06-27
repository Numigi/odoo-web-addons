# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    def _get_default_website(self):
        return self.env["website"].search([("default_website", "=", True)])

    website_ids = fields.Many2many(
        "website",
        "website_users_rel",
        "user_id",
        "wid",
        default=_get_default_website,
        string="Allowed Websites",
        help="Restrict user access to specific websites.",
    )
    websites_count = fields.Integer(
        compute="_compute_websites_count", string="Number of Websites"
    )

    def _compute_websites_count(self):
        self.websites_count = self.env["website"].sudo().search_count([])
