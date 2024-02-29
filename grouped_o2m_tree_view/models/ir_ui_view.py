# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def postprocess(self, model, node, view_id, in_tree_view, model_fields):
        if node.tag == 'field' and node.attrib.get('widget') == 'grouped_o2many_tree':
            group_by = node.attrib.get('group_by')
            field_name = node.attrib.get('name')
            if model_fields[field_name]['type'] != 'one2many':
                self.raise_view_error(_('grouped_o2many_tree is only supported for one2many fields !'), self.id)

            if not group_by:
                self.raise_view_error(_('"group_by" attribute is expected !'), self.id)

            if not (group_by in self.env[model_fields[field_name]['relation']]._fields):
                self.raise_view_error(_('"%s" has no attribute "%s" !') % (model_fields[field_name]['relation'], group_by), self.id)

            if isinstance(self.env[model_fields[field_name]['relation']]._fields[group_by], (fields.One2many, fields.Many2many)):
                self.raise_view_error(_('Group by field (%s) must not be a One2many or Many2many field !') % group_by, self.id)

        return super(View, self).postprocess(model, node, view_id, in_tree_view, model_fields)
