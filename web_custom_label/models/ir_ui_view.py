# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models
from .common import set_custom_labels_on_fields


class ViewWithCustomLabels(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        lang = self.env.context.get('lang') or self.env.user.lang
        labels = self.env['web.custom.label'].get(model, lang)
        arch_with_custom_labels = _add_custom_labels_to_view_arch(labels, arch)
        set_custom_labels_on_fields(labels, fields)
        return arch_with_custom_labels, fields


def _add_custom_labels_to_view_arch(labels, arch):
    labels_to_apply = [l for l in labels if l['position'] in ('string', 'placeholder', 'help')]

    if not labels_to_apply:
        return arch

    tree = etree.fromstring(arch)

    for label in labels_to_apply:
        _add_custom_label_to_view_tree(label, tree)

    return etree.tostring(tree)


def _add_custom_label_to_view_tree(label, tree):
    xpath_expr = (
        "//field[@name='{field_name}'] | //label[@for='{field_name}']"
        .format(field_name=label['reference'])
        if label['type_'] == 'field' else label['reference']
    )

    for element in tree.xpath(xpath_expr):
        element.attrib[label['position']] = label['term']
