# Copyright 2026 Numigi Solutions
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCarrierAccount(WebsiteSale):

    @route(["/shop/carrier_account/update"], type="json", auth="public", website=True)
    def update_carrier_account_number(self, carrier_account_number=None, **kw):
        """Update the carrier account number on the current portal quotation."""
        order = request.website.sale_get_order()
        if not order:
            return {"status": "error", "message": "No active sale order found"}

        order.set_carrier_account_number(carrier_account_number)
        return {"status": "success"}
