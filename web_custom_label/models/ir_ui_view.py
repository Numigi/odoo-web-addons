# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import models
from .common import set_custom_labels_on_fields


class ViewWithCustomLabels(models.Model):

    _inherit = "ir.ui.view"

    def postprocess_and_fields(self, node, model=None, **options):
        arch = node
        lang = self.env.context.get("lang") or self.env.user.lang
        labels = self.env["web.custom.label"].get(model, lang)

        arch_with_custom_labels = _add_custom_labels_to_view_arch(labels, arch)
        return super().postprocess_and_fields(
            arch_with_custom_labels, model=model, **options
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
        lang = self.env.context.get("lang") or self.env.user.lang
        labels = self.env["web.custom.label"].get(model_name, lang)
        set_custom_labels_on_fields(labels, name_manager.available_fields)
        return name_manager


def _add_custom_labels_to_view_arch(labels, arch):
    labels_to_apply = [
        label
        for label in labels
        if label["position"] in ("string", "placeholder", "help")
    ]

    if not labels_to_apply:
        return arch

    arch_string = etree.tostring(arch, encoding="unicode")
    tree = etree.fromstring(arch_string)

    for label in labels_to_apply:
        _add_custom_label_to_view_tree(label, tree)

    return tree


def _add_custom_label_to_view_tree(label, tree):
    xpath_expr = (
        "//field[@name='{field_name}'] | //label[@for='{field_name}']".format(
            field_name=label["reference"]
        )
        if label["type_"] == "field"
        else label["reference"]
    )

    for element in tree.xpath(xpath_expr):
        element.attrib[label["position"]] = label["term"]
