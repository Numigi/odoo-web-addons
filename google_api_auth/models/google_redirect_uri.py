# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class GoogleRedirectUri(models.Model):
    _name = "google.redirect.uri"
    _description = "Google Application Redirect URI"

    name = fields.Char(string="URL", required=True)
    google_application_id = fields.Many2one("google.application", string="Google Application", readonly=True, ondelete="cascade")
