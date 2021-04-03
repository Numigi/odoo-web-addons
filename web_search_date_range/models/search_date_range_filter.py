# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SearchDateRangeFilter(models.Model):

    _name = 'search.date.range.filter'
    _description = 'Date Filter'
    _order = 'model_id, field_id, sequence'

    sequence = fields.Integer(related='range_id.sequence', store=True)
    model_id = fields.Many2one('ir.model', 'Model', ondelete='cascade', required=True)
    field_id = fields.Many2one(
        'ir.model.fields', 'Field', ondelete='cascade', required=True,
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['date', 'datetime'])]",
    )
    range_id = fields.Many2one('search.date.range', 'Range Type', required=True)
    domain = fields.Text(compute='_compute_domain')

    @api.onchange('model_id')
    def _onchange_model_id_empty_field_id(self):
        self.field_id = None

    @api.depends('range_id', 'field_id')
    def _compute_domain(self):
        for line in self.filtered(lambda l: l.range_id and l.field_id):
            line.domain = f'[("{line.field_id.name}", "range", {line.range_id.id})]'

    @api.model
    def get_filter_list(self):
        return [
            {
                "isRelativeDateFilter": True,
                "description": field.field_description,
                "type": "filter",
                "model": field.model,
                "field": field.name,
                "options": [
                    l._get_option() for l in lines
                ]
            }
            for field, lines in self.search([])._group_by_field()
        ]

    def _group_by_field(self):
        groups = {}

        for line in self:
            if line.field_id not in groups:
                groups[line.field_id] = line
            else:
                groups[line.field_id] |= line

        return groups.items()

    def _get_option(self):
        return {
            "id": f"date_range_filter_{self.id}",
            "domain": self.domain,
            "description": self.range_id.label,
        }
