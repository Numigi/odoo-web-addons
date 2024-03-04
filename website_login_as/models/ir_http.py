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
            request.website_routing = request.env["website"].get_current_website(
            ).id
            rule, arguments = cls._match(request.httprequest.path)
            func = rule.endpoint
            return func.routing.get("website", False)
        except Exception:
            return True

    @classmethod
    def _dispatch(cls):
        if cls._website_enabled():
            context = dict(request.context)

            if not request.uid and request.context.get("uid"):
                user = request.env["res.users"].browse(request.context["uid"])
            else:
                user = request.env.user

            if user:
                cls._handle_request_context(user, context)
                if request.context.get("login_as"):
                    request.uid = request.context.get("login_as")
                else:
                    request.uid = user.id
        return super(Http, cls)._dispatch()

    @classmethod
    def _handle_request_context(cls, user, context):
        if not request.context.get("login_as"):
            context.update({'login_as': user.login_as_user_id.id or user.id})
            request.context = context
