# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import datetime
import pytz

from ddt import data, ddt
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

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
        date_range = self.env.ref('web_search_date_range.{range_ref}'.format(range_ref=range_ref))
        return self.env['search.date.range.filter'].create({
            'model_id': self.model.id,
            'field_id': self.field.id,
            'range_id': date_range.id,
        })

    def _eval_filter_domain(self, range_ref):
        date_filter = self._generate_filter(range_ref)
        return safe_eval(date_filter.domain, {
            'context_today': lambda: datetime.datetime.now(pytz.utc),
            'datetime': datetime,
            'relativedelta': relativedelta,
        })

    def test_eval_domain_for_range_before_today(self):
        with freeze_time('2018-05-18'):
            domain = self._eval_filter_domain('range_before_today')
            self.assertEqual(domain, [
                ('create_date', '<', '2018-05-18'),
            ])

    def test_eval_domain_for_range_today(self):
        with freeze_time('2018-05-18'):
            domain = self._eval_filter_domain('range_today')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-18'),
                ('create_date', '<', '2018-05-19'),
            ])

    def test_eval_domain_for_next_fifteen_days(self):
        with freeze_time('2018-05-18'):
            domain = self._eval_filter_domain('range_next_fifteen_days')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-18'),
                ('create_date', '<', '2018-06-02'),
            ])

    @data('2018-05-14', '2018-05-18', '2018-05-20')
    def test_eval_domain_for_range_current_week(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_current_week')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-14'),
                ('create_date', '<', '2018-05-21'),
            ])

    @data('2018-05-14', '2018-05-18', '2018-05-20')
    def test_eval_domain_for_range_next_week(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_next_week')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-21'),
                ('create_date', '<', '2018-05-28'),
            ])

    @data('2018-05-14', '2018-05-18', '2018-05-20')
    def test_eval_domain_for_range_previous_week(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_previous_week')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-07'),
                ('create_date', '<', '2018-05-14'),
            ])

    @data('2018-05-01', '2018-05-18', '2018-05-31')
    def test_eval_domain_for_range_current_month(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_current_month')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-05-01'),
                ('create_date', '<', '2018-06-01'),
            ])

    @data('2018-05-01', '2018-05-18', '2018-05-31')
    def test_eval_domain_for_range_next_month(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_next_month')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-06-01'),
                ('create_date', '<', '2018-07-01'),
            ])

    @data('2018-05-01', '2018-05-18', '2018-05-31')
    def test_eval_domain_for_range_previous_month(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_previous_month')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-04-01'),
                ('create_date', '<', '2018-05-01'),
            ])

    @data('2018-01-01', '2018-05-18', '2018-12-31')
    def test_eval_domain_for_range_current_year(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_current_year')
            self.assertEqual(domain, [
                ('create_date', '>=', '2018-01-01'),
                ('create_date', '<', '2019-01-01'),
            ])

    @data('2018-01-01', '2018-05-18', '2018-12-31')
    def test_eval_domain_for_range_next_year(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_next_year')
            self.assertEqual(domain, [
                ('create_date', '>=', '2019-01-01'),
                ('create_date', '<', '2020-01-01'),
            ])

    @data('2018-01-01', '2018-05-18', '2018-12-31')
    def test_eval_domain_for_range_previous_year(self, today):
        with freeze_time(today):
            domain = self._eval_filter_domain('range_previous_year')
            self.assertEqual(domain, [
                ('create_date', '>=', '2017-01-01'),
                ('create_date', '<', '2018-01-01'),
            ])
