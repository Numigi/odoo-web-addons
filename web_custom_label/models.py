# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from typing import List, Mapping
from odoo import api, fields, models, modules, tools
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
    active = fields.Boolean(default=True)


class WebCustomLabelWithCachedLabels(models.Model):
    """Add a cache for getting the labels.

    Searching the labels using the Odoo orm has an high cost in performance.
    Therefore, the labels are cached per model and language.

    The system cache is invalidated when any label record is added / modified / deleted.
    """

    _inherit = 'web.custom.label'

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return new_record

    @api.multi
    def write(self, vals):
        super().write(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @api.multi
    def unlink(self):
        super().unlink()
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @tools.ormcache('model', 'lang')
    def _find_labels(self, model, lang):
        """Find the labels matching the given model and lang code.

        :param model: the name of the model.
        :param lang: the language code
        :return: a list of custom labels values (list of dictionaries)
        """
        return self.sudo().env['web.custom.label'].search([
            ('model_ids.model', '=', model),
            ('lang', '=', lang),
        ]).read()


class ViewWithCustomLabels(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        lang = self.env.context.get('lang') or self.env.user.lang
        labels = self.env['web.custom.label']._find_labels(model, lang)
        arch_with_custom_labels = add_custom_labels_to_view_arch(labels, arch)
        set_custom_labels_on_fields(labels, fields)
        return arch_with_custom_labels, fields


class BaseWitCustomLabels(models.AbstractModel):

    _inherit = 'base'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Add the custom labels to the fields metadata.

        The method is used to query the fields metadata.
        This data is used by search filters / group by to display the field names.
        """
        fields = super().fields_get(allfields, attributes)
        lang = self.env.context.get('lang') or self.env.user.lang
        labels = self.env['web.custom.label']._find_labels(self._name, lang)
        set_custom_labels_on_fields(labels, fields)
        return fields


def add_custom_labels_to_view_arch(labels: List[dict], arch: str) -> str:
    """Add custom labels to the given view architecture.

    :param arch: the architecture to extend.
    :param labels: a list of custom labels to apply.
    :return: the view architecture with custom labels.
    """
    if not labels:
        return arch

    tree = etree.fromstring(arch)

    for label in labels:
        _add_custom_label_to_view_tree(label, tree)

    return etree.tostring(tree)


def _add_custom_label_to_view_tree(label: dict, tree: etree._Element):
    """Add a custom label to the given view architecture.

    :param label: the label to add to the view.
    :param tree: the etree.Element of the view to extend.
    """
    xpath_expr = (
        "//field[@name='{field_name}'] | //label[@for='{field_name}']"
        .format(field_name=label['reference'])
        if label['type_'] == 'field' else label['reference']
    )

    for element in tree.xpath(xpath_expr):
        element.attrib[label['position']] = label['term']


def set_custom_labels_on_fields(labels: List[dict], fields: Mapping[str, dict]) -> str:
    """Set the custom labels on the related fields.

    :param labels: a list of custom labels to apply.
    :param fields: the dict of fields data to extend.
    """
    field_labels = (l for l in labels if l['type_'] == 'field' and l['position'] == 'string')
    for label in field_labels:
        field = fields.get(label['reference'])
        if field:
            field['string'] = label['term']
