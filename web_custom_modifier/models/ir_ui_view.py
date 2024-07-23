# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from lxml import etree
from odoo import models
from odoo.addons.base.models.ir_ui_view import NameManager

from .common import set_custom_modifiers_on_fields

STANDARD_MODIFIERS = (
    "invisible",
    "column_invisible",
    "readonly",
    "required",
)


class ViewWithCustomModifiers(models.Model):
    _inherit = "ir.ui.view"

    def postprocess_and_fields(self, node, model=None, **options):
        modifiers = self.env["web.custom.modifier"].get(model)
        node_with_custom_modifiers = _add_custom_modifiers_to_view_arch(modifiers, node)
        self.clear_caches()  # Clear the cache in order to recompute _get_active_rules
        return super().postprocess_and_fields(
            node_with_custom_modifiers, model, **options
        )

    def _postprocess_view(
        self, node, model_name, editable=True, parent_name_manager=None, **options
    ):
        name_manager = super()._postprocess_view(
            node,
            model_name,
            editable=editable,
            parent_name_manager=parent_name_manager,
            **options
        )
        modifiers = self.env["web.custom.modifier"].get(model_name)
        set_custom_modifiers_on_fields(modifiers, name_manager.available_fields)
        return name_manager


def _add_custom_modifiers_to_view_arch(modifiers, arch):
    """Add custom modifiers to the given view architecture."""
    if not modifiers:
        return arch
    for modifier in modifiers:
        _add_custom_modifier_to_view_tree(modifier, arch)
    return arch


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
    key = modifier["modifier"]
    if key == "widget":
        node.attrib["widget"] = modifier["key"]

    if key == "optional":
        node.attrib["optional"] = modifier["key"]

    elif key == "force_save":
        node.attrib["force_save"] = "1"

    elif key == "limit":
        node.attrib["limit"] = modifier["key"]

    elif key in STANDARD_MODIFIERS:
        node.set(key, "1")
        modifiers = _get_node_modifiers(node)
        modifiers[key] = True
        _set_node_modifiers(modifiers, node)


def _get_node_modifiers(node):
    modifiers = node.get("modifiers")
    return json.loads(modifiers) if modifiers else {}


def _set_node_modifiers(modifiers, node):
    node.set("modifiers", json.dumps(modifiers))
