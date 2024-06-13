# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    allowed_website_ids = fields.Many2many(
        "website",
        string="Websites",
        store=True,
        readonly=False,
        help="Restrict user access to specific websites.",
    )

    def _get_default_website(self):
        return self.env["website"].search([("default_website", "=", True)])

    # Do onchange
    @api.onchange("partner_id", "partner_id.type")
    def _onchange_partner_type(self):
        if self.partner_id.type in ["portal", "public"]:
            # For portal users and public users, we want to allow access
            # to the default website by default.
            # if self.has_group("base.group_portal") or self.has_group("base.group_public"):
            self.allowed_website_ids = self._get_default_website()

        # if self.has_group("base.group_portal") or user.has_group(
        #     "base.group_public"
        # ):
        #     user.allowed_website_ids = self.env["website"].search(
        #         [("default_website", "=", True)]
        #         )
