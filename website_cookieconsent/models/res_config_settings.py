# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_cookieconsent_enabled = fields.Boolean(
        related="website_id.cookieconsent_enabled",
        string="Use CookieConsent",
        readonly=False,
    )
