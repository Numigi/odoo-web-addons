# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytz

from ddt import data, ddt, unpack
from dateutil.relativedelta import relativedelta
from datetime import datetime
from freezegun import freeze_time
from odoo.tests import common
from odoo.tools.safe_eval import safe_eval


@ddt
class TestSearchDateRange(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = cls.env.ref("base.model_res_partner")
        cls.field = cls.env.ref("base.field_res_partner__create_date")
        cls.env.user.company_id.write(
            {"fiscalyear_last_month": "3", "fiscalyear_last_day": "31",}
        )

    def _eval_filter_domain(self, range_ref):
        date_range = self.env.ref(f"web_search_date_range_account.{range_ref}")
        return date_range.generate_domain(self.field.name)

    @data(
        ("2018-03-31", "2016-04-01", "2017-04-01"),
        ("2018-04-01", "2017-04-01", "2018-04-01"),
    )
    @unpack
    def test_range_previous_fiscal_year(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_previous_fiscal_year")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )

    @data(
        ("2018-03-31", "2017-04-01", "2018-04-01"),
        ("2018-04-01", "2018-04-01", "2019-04-01"),
    )
    @unpack
    def test_range_current_fiscal_year(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_current_fiscal_year")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )

    @data(
        ("2018-03-31", "2018-04-01", "2019-04-01"),
        ("2018-04-01", "2019-04-01", "2020-04-01"),
    )
    @unpack
    def test_range_next_fiscal_year(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_next_fiscal_year")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )

    @data(
        ("2018-03-31", "2017-10-01", "2018-01-01"),
        ("2018-04-01", "2018-01-01", "2018-04-01"),
    )
    @unpack
    def test_range_previous_trimester(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_previous_trimester")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )

    @data(
        ("2018-03-31", "2018-01-01", "2018-04-01"),
        ("2018-04-01", "2018-04-01", "2018-07-01"),
    )
    @unpack
    def test_range_current_trimester(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_current_trimester")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )

    @data(
        ("2018-03-31", "2018-04-01", "2018-07-01"),
        ("2018-04-01", "2018-07-01", "2018-10-01"),
    )
    @unpack
    def test_range_next_trimester(self, today, date_from, date_to):
        with freeze_time(today):
            domain = self._eval_filter_domain("range_next_trimester")

        self.assertEqual(
            domain,
            [
                "&",
                ("create_date", ">=", date_from),
                ("create_date", "<", date_to),
            ],
        )
