# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class SearchDateRange(models.Model):

    _name = "search.date.range"
    _description = "Date Range"
    _rec_name = "label"
    _order = "sequence"

    sequence = fields.Integer()
    label = fields.Char(translate=True, required=True)
    domain = fields.Text(required=True)
    xml_id = fields.Many2one("ir.model.data", "XML ID", compute="_compute_xml_id")
    noupdate = fields.Boolean(
        "No Update", compute="_compute_noupdate", inverse="_set_noupdate"
    )

    def _compute_xml_id(self):
        for range_type in self:
            range_type.xml_id = self.env["ir.model.data"].search(
                [
                    ("model", "=", range_type._name),
                    ("res_id", "=", range_type.id),
                    ("module", "!=", False),
                ],
                limit=1,
            )

    def _compute_noupdate(self):
        for range_type in self:
            range_type.noupdate = (
                range_type.xml_id.noupdate if range_type.xml_id else False
            )

    def _set_noupdate(self):
        range_types_with_xml_id = self.filtered(lambda r: r.xml_id)
        for range_type in range_types_with_xml_id:
            range_type.xml_id.noupdate = range_type.noupdate

    def generate_domain(self, field):
        return safe_eval(self.domain, self._get_domain_context(field))

    @api.model
    def _get_domain_context(self, field):
        return {
            "field": field,
            "today": fields.Date.context_today(self),
            "datetime": datetime,
            "relativedelta": relativedelta,
            "MO": MO,
            "TU": TU,
            "WE": WE,
            "TH": TH,
            "FR": FR,
            "SA": SA,
            "SU": SU,
        }
