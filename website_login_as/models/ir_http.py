# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class Http(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _website_enabled(cls):
        try:
            request.website_routing = request.env["website"].get_current_website().id
            rule, arguments = cls._match(request.httprequest.path)
            func = rule.endpoint
            return func.routing.get("website", False)
        except Exception as e:
            return True

    @classmethod
    def _dispatch(cls):
        if cls._website_enabled():
            if not request.uid and request.context.get("uid"):
                user = request.env["res.users"].browse(request.context["uid"])
            else:
                user = request.env.user
            if user:
                request.uid = user.login_as_user_id.id or user.id

        return super(Http, cls)._dispatch()
