# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from .common import set_custom_modifiers_on_fields


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Add the custom modifiers to the fields metadata."""
        fields_dict = super().fields_get(allfields, attributes)
        modifiers = self.env["web.custom.modifier"].get(self._name)
        if modifiers:
            set_custom_modifiers_on_fields(modifiers, fields_dict)
        return fields_dict


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
