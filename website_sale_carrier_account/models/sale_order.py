# Copyright 2026 Numigi Solutions
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    carrier_account_number = fields.Char(
        string="Carrier Account Number",
        copy=False,
    )

    def set_carrier_account_number(self, account_number):
        """Store carrier account number and append it to sale order notes."""
        self.ensure_one()
        self.carrier_account_number = account_number
        if account_number:
            lang = self.partner_id.lang or self.env.user.lang
            order = self.with_context(lang=lang)
            formatted_note = order._format_carrier_note(account_number)
            order._append_carrier_note(formatted_note)
            order.message_post(body=formatted_note)

    def _format_carrier_note(self, account_number):
        """Return the carrier note text translated in the context language."""
        return _("Carrier Account Number: %s") % account_number

    def _append_carrier_note(self, note_text):
        """Append text to the sale order note field safely."""
        if not self.note:
            self.note = f"\n{note_text}"
            return

        if note_text not in self.note:
            self.note = f"{self.note}\n{note_text}"
