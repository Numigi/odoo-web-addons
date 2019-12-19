# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from typing import List
from odoo import api, models
from odoo.osv.orm import transfer_node_to_modifiers, transfer_modifiers_to_node


def _add_custom_modifier_to_view_tree(modifier: dict, tree: etree._Element):
    """Add a custom modifier to the given view architecture.

    :param modifier: the modifier to add to the view.
    :param tree: the etree.Element of the view to extend.
    """
    xpath_expr = (
        "//field[@name='{field_name}'] | //modifier[@for='{field_name}']"
        .format(field_name=modifier['reference'])
        if modifier['type_'] == 'field' else modifier['reference']
    )

    for node in tree.xpath(xpath_expr):
        modifiers = {}
        transfer_node_to_modifiers(node, modifiers)
        modifiers[modifier['modifier']] = True
        transfer_modifiers_to_node(modifiers, node)


def _add_custom_modifiers_to_view_arch(modifiers: List[dict], arch: str) -> str:
    """Add custom modifiers to the given view architecture.

    :param arch: the architecture to extend.
    :param modifiers: a list of custom modifiers to apply.
    :return: the view architecture with custom modifiers.
    """
    if not modifiers:
        return arch

    tree = etree.fromstring(arch)

    for modifier in modifiers:
        _add_custom_modifier_to_view_tree(modifier, tree)

    return etree.tostring(tree)


class ViewWithCustomModifiers(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom modifiers to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        modifiers = self.env['web.custom.modifier']._find_modifiers(model)
        arch_with_custom_modifiers = _add_custom_modifiers_to_view_arch(modifiers, arch)
        return arch_with_custom_modifiers, fields
