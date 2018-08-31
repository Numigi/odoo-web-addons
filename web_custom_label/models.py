# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, fields, models
from odoo.addons.base.res.res_partner import _lang_get


class WebCustomLabel(models.Model):

    _name = 'web.custom.label'
    _description = 'Custom View Label'

    lang = fields.Selection(
        _lang_get, 'Language', default=lambda self: self.env.lang,
        required=True,
    )
    model_ids = fields.Many2many(
        'ir.model', 'ir_model_custom_label', 'label_id', 'model_id', 'Model')
    type_ = fields.Selection([
        ('field', 'Field'),
        ('xpath', 'Xpath'),
    ], default='field', required=True)
    position = fields.Selection([
        ('string', 'Label'),
        ('placeholder', 'Placeholder'),
    ], default='string', required=True)
    reference = fields.Char(required=True)
    term = fields.Char(required=True)


class ViewWithCustomLabels(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        lang = self.env.context.get('lang') or self.env.user.lang
        arch_with_custom_labels = add_custom_labels_to_view_arch(self.env, model, lang, arch)
        return arch_with_custom_labels, fields


def add_custom_labels_to_view_arch(env: api.Environment, model: str, lang: str, arch: str) -> str:
    """Add custom labels to the given view architecture.

    :param env: the Odoo environment.
    :param model: the name of the model.
    :param lang: the language of the labels to add.
    :param arch: the architecture to extend.
    :return: the view architecture with custom labels.
    """
    labels = env['web.custom.label'].search([
        ('model_ids.model', '=', model),
        ('lang', '=', lang),
    ])

    if not labels:
        return arch

    tree = etree.fromstring(arch)

    for label in labels:
        _add_custom_label_to_view_tree(label, tree)

    return etree.tostring(tree)


def _add_custom_label_to_view_tree(label: WebCustomLabel, tree):
    """Add a custom label to the given view architecture.

    :param label: the label to add to the view.
    :param tree: the etree.Element of the view to extend.
    """
    xpath_expr = (
        "//field[@name='{field_name}'] | //label[@for='{field_name}']"
        .format(field_name=label.reference)
        if label.type_ == 'field' else label.reference
    )

    for element in tree.xpath(xpath_expr):
        element.attrib[label.position] = label.term
