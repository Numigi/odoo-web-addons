from odoo import fields, models

class Website(models.Model):
    _inherit = "website"

    cookieconsent_enabled = fields.Boolean(
        string="Use CookieConsent",
        help="Display a cookie banner on your website."
    )
