# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class Partner(models.Model):
    _inherit = "res.partner"

    def _compute_display_name(self):
        """
        This avoid to load removed selection option in modifiers
        that would raise an error when trying to display them. Display instead,
        the name of the record.
        This could be improved or fixed for each case if needed.
        """
        try:
            super()._compute_display_name()
        except Exception:
            for partner in self:
                partner.display_name = partner.name
