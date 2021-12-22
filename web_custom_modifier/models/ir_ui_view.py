# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models
from odoo.addons.base.models.ir_ui_view import (
    transfer_node_to_modifiers,
    transfer_modifiers_to_node,
)
from .common import set_custom_modifiers_on_fields


STANDARD_MODIFIERS = ("invisible" "column_invisible" "readonly" "force_save" "required")


class ViewWithCustomModifiers(models.Model):

    _inherit = "ir.ui.view"

    def postprocess_and_fields(self, node, model=None, validate=False):
        """Add custom modifiers to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(node, model, validate)

        view_model = model or self.model
        if view_model:
            modifiers = self.env["web.custom.modifier"].get(view_model)
            arch_with_custom_modifiers = _add_custom_modifiers_to_view_arch(modifiers, arch)
            set_custom_modifiers_on_fields(modifiers, fields)

        return arch_with_custom_modifiers, fields


def _add_custom_modifiers_to_view_arch(modifiers, arch):
    """Add custom modifiers to the given view architecture."""
    if not modifiers:
        return arch

    tree = etree.fromstring(arch)

    for modifier in modifiers:
        _add_custom_modifier_to_view_tree(modifier, tree)

    return etree.tostring(tree)


def _add_custom_modifier_to_view_tree(modifier, tree):
    """Add a custom modifier to the given view architecture."""
    xpath_expr = (
        "//field[@name='{field_name}'] | //modifier[@for='{field_name}']".format(
            field_name=modifier["reference"]
        )
        if modifier["type_"] == "field"
        else modifier["reference"]
    )

    for node in tree.xpath(xpath_expr):
        _add_custom_modifier_to_node(node, modifier)


def _add_custom_modifier_to_node(node, modifier):
    key = modifier['modifier']

    if key == "widget":
        node.attrib["widget"] = modifier["key"]

    elif key in STANDARD_MODIFIERS:
        modifiers = {}
        transfer_node_to_modifiers(node, modifiers)
        modifiers[modifier['modifier']] = True
        transfer_modifiers_to_node(modifiers, node)
