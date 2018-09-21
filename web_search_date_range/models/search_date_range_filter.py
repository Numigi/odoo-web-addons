# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SearchDateRangeFilter(models.Model):
    """A model used to define date range filters on models."""

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
    domain = fields.Text(compute='_compute_domain', store=True)

    @api.onchange('model_id')
    def _onchange_model_id_empty_field_id(self):
        self.field_id = None

    @api.depends('range_id.domain', 'field_id')
    def _compute_domain(self):
        lines_with_range_and_field = self.filtered(lambda l: l.range_id and l.field_id)
        for line in lines_with_range_and_field:
            line.domain = line.range_id.generate_domain_from_field_name(line.field_id.name)

    @api.model
    def get_filter_list(self):
        """Get a complete list of filter values to display in the web interface."""
        return [
            {
                'model': line.field_id.model,
                'field': line.field_id.name,
                'domain': line.domain,
                'sequence': line.sequence,
                'label': line.range_id.label,
                'field_label': line.field_id.field_description,
                'technical_name': 'filter_range_{range}_{field}'.format(
                    range=line.range_id.technical_name, field=line.field_id.name)
            }
            for line in self.with_context(lang=self.env.user.lang).search([])
        ]
