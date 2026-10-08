# Copyright 2026 Numigi Solutions
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    has_carrier_number = fields.Boolean(
        string="Carrier Account Number Required",
        help="If checked, the customer can enter their carrier account number at checkout.",
    )
