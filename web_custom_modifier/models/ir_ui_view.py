# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from lxml import etree
from odoo import api, models
from .common import set_custom_modifiers_on_fields


STANDARD_MODIFIERS = ("invisible" "column_invisible" "readonly" "force_save" "required")


class ViewWithCustomModifiers(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom modifiers to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        modifiers = self.env['web.custom.modifier'].get(model)
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
        "//field[@name='{field_name}'] | //modifier[@for='{field_name}']"
        .format(field_name=modifier['reference'])
        if modifier['type_'] == 'field' else modifier['reference']
    )

    for node in tree.xpath(xpath_expr):
        _add_custom_modifier_to_node(node, modifier)


def _add_custom_modifier_to_node(node, modifier):
    key = modifier['modifier']

    if key == "widget":
        node.attrib["widget"] = modifier["key"]

    elif key in STANDARD_MODIFIERS:
        modifiers = _get_node_modifiers(node)
        modifiers[key] = True
        _set_node_modifiers(modifiers, node)


def _get_node_modifiers(node):
    modifiers = node.get('modifiers')
    return json.loads(modifiers) if modifiers else {}


def _set_node_modifiers(modifiers, node):
    node.set('modifiers', json.dumps(modifiers))
