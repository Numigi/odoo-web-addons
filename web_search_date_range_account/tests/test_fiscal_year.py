# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import data, ddt, unpack
from freezegun import freeze_time
from odoo import fields
from odoo.tests import common


@ddt
class TestSessionInfo(common.TransactionCase):

    @data(
        ('2018-01-01', 12, 31, '2018-01-01'),
        ('2018-05-15', 12, 31, '2018-01-01'),
        ('2018-12-31', 12, 31, '2018-01-01'),
        ('2018-02-28', 2, 29, '2017-03-01'),
        ('2018-03-01', 2, 29, '2018-03-01'),
        ('2018-12-31', 2, 29, '2018-03-01'),
        ('2018-02-01', 11, 30, '2017-12-01'),
        ('2018-03-01', 11, 30, '2017-12-01'),
        ('2018-12-31', 11, 30, '2018-12-01'),
    )
    @unpack
    def test_fiscal_year_start(self, today, last_month, last_day, year_start):
        today = fields.Date.to_date(today)
        year_start = fields.Date.to_date(year_start)

        self.env.user.company_id.write({
            'fiscalyear_last_month': str(last_month),
            'fiscalyear_last_day': str(last_day),
        })

        with freeze_time(today):
            context = self._get_domain_context()
            assert context['fiscal_year_start'] == year_start

    @data(
        ('2018-01-01', 12, 31, '2018-01-01'),
        ('2018-05-15', 12, 31, '2018-04-01'),
        ('2018-12-31', 12, 31, '2018-10-01'),
        ('2018-02-01', 2, 29, '2017-12-01'),
        ('2018-03-01', 2, 29, '2018-03-01'),
        ('2018-12-31', 2, 29, '2018-12-01'),
        ('2018-11-30', 11, 30, '2018-09-01'),
        ('2018-03-01', 11, 30, '2018-03-01'),
        ('2018-12-31', 11, 30, '2018-12-01'),
        ('2018-07-15', 11, 30, '2018-06-01'),
    )
    @unpack
    def test_trimester_start(self, today, last_month, last_day, year_start):
        today = fields.Date.to_date(today)
        year_start = fields.Date.to_date(year_start)

        self.env.user.company_id.write({
            'fiscalyear_last_month': str(last_month),
            'fiscalyear_last_day': str(last_day),
        })

        with freeze_time(today):
            context = self._get_domain_context()
            assert context['trimester_start'] == year_start

    def _get_domain_context(self):
        return self.env["search.date.range"]._get_domain_context("date")
