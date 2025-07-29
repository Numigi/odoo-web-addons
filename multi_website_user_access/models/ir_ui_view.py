# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.http import request
from odoo.addons.website.models import ir_http


class IrUiView(models.Model):

    _inherit = "ir.ui.view"

    def _render(self, values=None, engine="ir.qweb", minimal_qcontext=False):
        is_frontend = ir_http.get_request_website()
        Website = self.env["website"]
        website_id = is_frontend and Website.get_current_website() or Website
        if website_id and website_id.id not in request.env.user.website_ids.ids:
            return super(
                IrUiView,
                self.browse(self.get_view_id("multi_website_user_access.page_403")),
            )._render(values, engine=engine, minimal_qcontext=minimal_qcontext)
        return super(IrUiView, self)._render(
            values=values, engine=engine, minimal_qcontext=minimal_qcontext
        )
