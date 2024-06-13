# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GoogleApplicationScope(models.Model):
    _name = "google.application.scope"
    _description = "Google Application Scopes"

    name = fields.Char(string="Scope", required=True)
    google_application_id = fields.Many2one(
        "google.application",
        string="Google Application",
        readonly=True,
        ondelete="cascade",
    )
