# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    login_as_user_id = fields.Many2one("res.users", "Login as")

    def login_as(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "/",
            "target": "new",
        }

    def logout_as(self):
        return self.write({"login_as_user_id": False})
