# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.http import request


class View(models.Model):

    _inherit = "ir.ui.view"

    def _render(self, values=None, engine="ir.qweb", minimal_qcontext=False):
        """
        Handle website page rendering if user is allowed to view it.
        Allow user portal page to be displayed.
        """
        if hasattr(request, "website") and hasattr(request, "httprequest"):
            if (
                request.httprequest.path.split("/")[1] != "my"
                and not request.website.is_public_user()
                and request.website.id not in request.env.user.allowed_website_ids.ids
            ):
                return super(
                    View,
                    self.browse(self.get_view_id("multi_website_user_access.page_403")),
                )._render(values, engine=engine, minimal_qcontext=minimal_qcontext)
        return super(View, self)._render(
            values, engine=engine, minimal_qcontext=minimal_qcontext
        )
