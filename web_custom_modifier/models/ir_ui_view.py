# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import models

STANDARD_MODIFIERS = (
    "invisible",
    "column_invisible",
    "readonly",
    "required",
)


class ViewWithCustomModifiers(models.Model):
    _inherit = "ir.ui.view"

    def postprocess_and_fields(self, node, model=None, **options):
        # Clear the cache in order to recompute active rules
        self.clear_caches()
        # In Odoo 18, it returns arch and models (not fields)
        arch, models_dict = super().postprocess_and_fields(node, model, **options)

        modifiers = self.env["web.custom.modifier"].get(model or self.model)
        if modifiers:
            _add_custom_modifiers_to_view_arch(modifiers, node)
            arch = etree.tostring(node, encoding="unicode").replace("\t", "")

        return arch, models_dict


def _add_custom_modifiers_to_view_arch(modifiers, node):
    """Add custom modifiers to the given view architecture."""
    for modifier in modifiers:
        _add_custom_modifier_to_view_tree(modifier, node)


def _add_custom_modifier_to_view_tree(modifier, node):
    """Add a custom modifier to the given view architecture."""
    xpath_expr = (
        "//field[@name='{field_name}'] | //modifier[@for='{field_name}']".format(
            field_name=modifier["reference"]
        )
        if modifier["type_"] == "field"
        else modifier["reference"]
    )
    for target_node in node.xpath(xpath_expr):
        _add_custom_modifier_to_node(target_node, modifier)


def _add_custom_modifier_to_node(node, modifier):
    key = modifier["modifier"]
    if key == "widget":
        node.attrib["widget"] = modifier["key"]

    elif key == "optional":
        node.attrib["optional"] = modifier["key"]

    elif key == "force_save":
        node.attrib["force_save"] = "1"

    elif key == "limit":
        node.attrib["limit"] = modifier["key"]

    elif key in STANDARD_MODIFIERS:
        # In Odoo 17/18, modifiers are standard string attributes evaluated client-side
        node.set(key, "True")
