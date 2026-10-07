# Copyright 2026 Numigi Solutions
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestCarrierAccount(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Customer"})
        self.carrier = self.env["delivery.carrier"].create(
            {
                "name": "Custom Transporter",
                "product_id": self.env.ref("delivery.product_product_delivery").id,
                "has_carrier_number": True,
            }
        )
        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )

    def test_set_carrier_account_number(self):
        self.sale_order.set_carrier_account_number("TR-123456")
        assert self.sale_order.carrier_account_number == "TR-123456"

    def test_carrier_account_number_appended_to_note(self):
        self.sale_order.set_carrier_account_number("TR-123456")
        assert "Carrier Account Number: TR-123456" in self.sale_order.note
