# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from .common import set_custom_modifiers_on_fields


class Base(models.AbstractModel):

    _inherit = "base"

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Add the custom modifiers to the fields metadata."""
        fields = super().fields_get(allfields, attributes)
        modifiers = self.env["web.custom.modifier"].get(self._name)
        set_custom_modifiers_on_fields(modifiers, fields)
        return fields


class Partner(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        """
        This avoid to load removed selection option in modifiers
        that would raise an error when trying to display them. Display instead,
        the name of the record.
        This could be improved or fixed for each case if needed.
        """
        try:
            res = super().name_get()
        except:  # noqa: E722
            res = []
            for partner in self:
                name = partner.name
                res.append((partner.id, name))
        return res
