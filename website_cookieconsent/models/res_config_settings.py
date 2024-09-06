from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("website_id.cookieconsent_enabled")
    def _compute_cookieconsent_enabled(self):
        for record in self:
            record.update({"cookieconsent_enabled": True})

    def _inverse_cookieconsent_enabled(self):
        for record in self:
            record.website_id.update({"cookieconsent_enabled": False})

    website_cookieconsent_enabled = fields.Boolean(
        related="website_id.cookieconsent_enabled",
        string="Use CookieConsent",
        compute="_compute_cookieconsent_enabled",
        inverse="_inverse_cookieconsent_enabled",
    )
