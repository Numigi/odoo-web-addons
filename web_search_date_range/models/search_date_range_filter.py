# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SearchDateRangeFilter(models.Model):

    _name = "search.date.range.filter"
    _description = "Date Filter"
    _order = "model_id, field_id"

    model_id = fields.Many2one("ir.model", "Model", ondelete="cascade", required=True)
    field_id = fields.Many2one(
        "ir.model.fields",
        "Field",
        ondelete="cascade",
        required=True,
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['date', 'datetime'])]",
    )
    range_ids = fields.Many2many(
        "search.date.range",
        "search_date_range_filter_rel",
        "filter_id",
        "range_id",
        string="Date Ranges",
        required=True,
    )

    @api.onchange("model_id")
    def _onchange_model_id_empty_field_id(self):
        self.field_id = None

    @api.model
    def get_filter_list(self):
        filters = [line._get_filter() for line in self.search([])]
        return sorted(filters, key=lambda f: f["description"])

    def _get_filter(self):
        return {
            "isRelativeDateFilter": True,
            "description": self.field_id.field_description,
            "type": "filter",
            "model": self.field_id.model,
            "field": self.field_id.name,
            "options": [self._get_option(range_) for range_ in self.range_ids],
        }

    def _get_option(self, range_):
        return {
            "id": f"date_range_filter_{self.id}_{range_.id}",
            "domain": self._get_domain(range_),
            "description": range_.label,
        }

    def _get_domain(self, range_):
        return f'[("{self.field_id.name}", "range", {range_.id})]'
