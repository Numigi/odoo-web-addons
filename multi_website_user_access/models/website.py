# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    default_website = fields.Boolean(
        "Default Website",
        help="Check this box to determine this website as the default value for \
            portal and public user access.",
    )
