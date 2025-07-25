# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    cookieconsent_enabled = fields.Boolean(
        string="Use CookieConsent", help="Display a cookie banner on your website."
    )
