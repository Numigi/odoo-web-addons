# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytz

from ddt import data, ddt
from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo.tests import common
from odoo.tools.safe_eval import safe_eval


@ddt
class TestSearchDateRange(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = cls.env.ref('base.model_res_partner')
        cls.field = cls.env.ref('base.field_res_partner_create_date')

    def _generate_filter(self, range_ref):
        date_range = self.env.ref(
            'web_search_date_range_account.{range_ref}'.format(range_ref=range_ref))
        return self.env['search.date.range.filter'].create({
            'model_id': self.model.id,
            'field_id': self.field.id,
            'range_id': date_range.id,
        })

    def _eval_filter_domain(self, range_ref, fiscal_year_start=None, trimester_start=None):
        date_filter = self._generate_filter(range_ref)
        return safe_eval(date_filter.domain, {
            'context_today': lambda: datetime.now(pytz.utc),
            'datetime': datetime,
            'relativedelta': relativedelta,
            'fiscal_year_start': (
                datetime.strptime(fiscal_year_start, '%Y-%m-%d') if fiscal_year_start else None
            ),
            'trimester_start': (
                datetime.strptime(trimester_start, '%Y-%m-%d') if trimester_start else None
            ),
        })

    @data(
        ("2018-01-01", '2017-01-01', '2018-01-01'),
        ("2018-02-01", '2017-02-01', '2018-02-01'),
        ("2016-03-01", '2015-03-01', '2016-03-01'),
        ("2017-03-01", '2016-03-01', '2017-03-01'),
        ("2018-03-01", '2017-03-01', '2018-03-01'),
        ("2018-12-01", '2017-12-01', '2018-12-01'),
    )
    def test_range_previous_fiscal_year(self, data):
        fiscal_year_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_previous_fiscal_year', fiscal_year_start=fiscal_year_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])

    @data(
        ("2018-01-01", '2018-01-01', '2019-01-01'),
        ("2018-02-01", '2018-02-01', '2019-02-01'),
        ("2016-03-01", '2016-03-01', '2017-03-01'),
        ("2017-03-01", '2017-03-01', '2018-03-01'),
        ("2018-03-01", '2018-03-01', '2019-03-01'),
        ("2018-12-01", '2018-12-01', '2019-12-01'),
    )
    def test_range_current_fiscal_year(self, data):
        fiscal_year_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_current_fiscal_year', fiscal_year_start=fiscal_year_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])

    @data(
        ("2018-01-01", '2019-01-01', '2020-01-01'),
        ("2018-02-01", '2019-02-01', '2020-02-01'),
        ("2016-03-01", '2017-03-01', '2018-03-01'),
        ("2017-03-01", '2018-03-01', '2019-03-01'),
        ("2018-03-01", '2019-03-01', '2020-03-01'),
        ("2018-12-01", '2019-12-01', '2020-12-01'),
    )
    def test_range_next_fiscal_year(self, data):
        fiscal_year_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_next_fiscal_year', fiscal_year_start=fiscal_year_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])

    @data(
        ("2018-01-01", '2017-10-01', '2018-01-01'),
        ("2018-02-01", '2017-11-01', '2018-02-01'),
        ("2016-03-01", '2015-12-01', '2016-03-01'),
        ("2017-03-01", '2016-12-01', '2017-03-01'),
        ("2018-03-01", '2017-12-01', '2018-03-01'),
        ("2018-12-01", '2018-09-01', '2018-12-01'),
    )
    def test_range_previous_trimester(self, data):
        trimester_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_previous_trimester', trimester_start=trimester_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])

    @data(
        ("2018-01-01", '2018-01-01', '2018-04-01'),
        ("2018-02-01", '2018-02-01', '2018-05-01'),
        ("2016-03-01", '2016-03-01', '2016-06-01'),
        ("2017-03-01", '2017-03-01', '2017-06-01'),
        ("2018-03-01", '2018-03-01', '2018-06-01'),
        ("2018-12-01", '2018-12-01', '2019-03-01'),
    )
    def test_range_current_trimester(self, data):
        trimester_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_current_trimester', trimester_start=trimester_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])

    @data(
        ("2018-01-01", '2018-04-01', '2018-07-01'),
        ("2018-02-01", '2018-05-01', '2018-08-01'),
        ("2016-03-01", '2016-06-01', '2016-09-01'),
        ("2017-03-01", '2017-06-01', '2017-09-01'),
        ("2018-03-01", '2018-06-01', '2018-09-01'),
        ("2018-12-01", '2019-03-01', '2019-06-01'),
    )
    def test_range_next_trimester(self, data):
        trimester_start, expected_date_from, expected_date_to = data
        domain = self._eval_filter_domain(
            'range_next_trimester', trimester_start=trimester_start)
        self.assertEqual(domain, [
            ('create_date', '>=', expected_date_from),
            ('create_date', '<', expected_date_to),
        ])
