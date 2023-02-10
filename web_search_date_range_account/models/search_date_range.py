# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class SearchDateRange(models.AbstractModel):

    _inherit = "search.date.range"

    @api.model
    def _get_domain_context(self, field):
        res = super()._get_domain_context(field)
        fiscal_year_start = self._get_fiscal_year_first_date()
        trimester_start = self._get_trimester_start(fiscal_year_start)
        res.update(
            fiscal_year_start=fiscal_year_start,
            trimester_start=trimester_start,
        )
        return res

    def _get_trimester_start(self, fiscal_year_start):
        months_passed = relativedelta(datetime.now(), fiscal_year_start).months
        return fiscal_year_start + relativedelta(
            months=3 * (months_passed // 3)
        )

    def _get_fiscal_year_first_date(self):
        today = fields.Date.context_today(self)
        last_month = int(self.env.user.company_id.fiscalyear_last_month)
        return (
            today
            + relativedelta(
                years=-1 if last_month >= today.month else 0, month=last_month, day=31
            )
            + timedelta(1)
        )
