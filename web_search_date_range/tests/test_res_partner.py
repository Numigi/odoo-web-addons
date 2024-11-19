# Copyright 2023-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
from datetime import datetime
from odoo.tests.common import TransactionCase


class TestPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.partner"].search([]).write({"date": False})

        cls.date_1 = datetime.now().date()
        cls.date_2 = cls.date_1 - relativedelta(days=30)

        cls.partner_1 = cls.env["res.partner"].create(
            {"name": "Partner 1", "date": cls.date_1}
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {"name": "Partner 1", "date": cls.date_2}
        )

    def test_search_partner(self):
        range_today = self.env.ref("web_search_date_range.range_today")

        with freeze_time(self.date_1):
            partners = self.env["res.partner"].search(
                [("date", "range", range_today.id)]
            )

        assert partners == self.partner_1
