# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import data, ddt
from freezegun import freeze_time

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
    def test_fiscal_year_start(self, data):
        today = data[0]
        self.env.user.company_id.fiscalyear_last_month = data[1]
        self.env.user.company_id.fiscalyear_last_day = data[2]
        expected_fiscal_year_start = data[3]

        with freeze_time(today):
            session_info = self.env['ir.http']._get_fiscal_year_info()
            assert session_info['fiscal_year_start'] == expected_fiscal_year_start

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
    def test_trimester_start(self, data):
        today = data[0]
        self.env.user.company_id.fiscalyear_last_month = data[1]
        self.env.user.company_id.fiscalyear_last_day = data[2]
        expected_trimester_start = data[3]

        with freeze_time(today):
            session_info = self.env['ir.http']._get_fiscal_year_info()
            assert session_info['trimester_start'] == expected_trimester_start
