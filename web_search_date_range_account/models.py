# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Http(models.AbstractModel):

    _inherit = 'ir.http'

    def session_info(self):
        """Add fiscal year details to the session info."""
        result = super().session_info()
        result.update(self._get_fiscal_year_info())
        return result

    def _get_fiscal_year_info(self):
        """Get the first day of the current fiscal year and financial trimester.

        :return: a dict containing the dates formated in standard Odoo date strings.
        """
        fiscal_year_start = self._get_fiscal_year_first_date()

        months_passed = relativedelta(datetime.now(), fiscal_year_start).months
        trimester_start = fiscal_year_start + relativedelta(months=3 * (months_passed // 3))

        return {
            'fiscal_year_start': fiscal_year_start.strftime(DEFAULT_SERVER_DATE_FORMAT),
            'trimester_start': trimester_start.strftime(DEFAULT_SERVER_DATE_FORMAT),
        }

    def _get_fiscal_year_first_date(self):
        """Get the first day of the fiscal year.

        :rtype: a datetime object
        """
        now = datetime.now()
        last_month = self.env.user.company_id.fiscalyear_last_month
        previous_year = now.year - 1 if last_month >= now.month else now.year
        previous_year_end = datetime(previous_year, 12, 31) - relativedelta(months=12 - last_month)
        return previous_year_end + timedelta(1)
