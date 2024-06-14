# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GoogleApplication(models.Model):
    _name = "google.application"
    _inherit = ["google.drive.mixin"]
    _description = "Google Application Information"

    def _check_active(self, vals):
        if vals.get("active", False) and self.search_count([("active", "=", True)]) > 0:
            raise ValidationError(_("Only one record can be active"))

    @api.model
    def create(self, vals):
        self._check_active(vals)
        return super(GoogleApplication, self).create(vals)

    def write(self, vals):
        self._check_active(vals)
        return super(GoogleApplication, self).write(vals)

    def get_access_token(self):
        self.ensure_one()
        if not self.access_token or self.token_expiry < fields.Datetime.now():
            self.button_refresh_token()
        return self.access_token
