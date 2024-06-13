# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import requests
import werkzeug
from datetime import datetime

from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_join
from datetime import timedelta

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class GoogleApplicationController(http.Controller):
    @http.route("/google_account/authentification", type="http", auth="user")
    def google_application_callback(self, code=None, state=None, error=None, **kwargs):
        """Callback URL during the OAuth process.

        Google redirects the user browser to this endpoint with the authorization code.
        We will fetch the refresh token and the access token thanks to this authorization
        code and save those values on the Google Application Parameters.
        """
        if not request.env.user.has_group("base.group_system"):
            _logger.error(
                "Google Application: non-system user trying to link an Google account."
            )
            raise Forbidden()

        if error:
            return _("An error occur during the authentication process.")

        # search for active Google application
        google_application = request.env["google.application"].search(
            [("active", "=", True)], limit=1
        )
        if not google_application:
            _logger.error("Google Application: No active Google application found.")
            raise Forbidden()
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        redirect_uri = url_join(base_url, "/google_account/authentification")

        data = {
            "client_id": google_application.client_id,
            "client_secret": google_application.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        headers = {
            "Host": "oauth2.googleapis.com",
            "Content-type": "application/x-www-form-urlencoded",
        }
        req = requests.post(google_application.token_uri, data=data, headers=headers)

        if req.status_code != 200:
            _logger.error(
                "Google Application: Error %s when fetching the access token.",
                req.status_code,
            )
            google_application.write({"status": "invalid"})
            raise Forbidden()

        response = req.json()
        date_expiration = datetime.now() + timedelta(seconds=response["expires_in"])

        google_application.write(
            {
                "code": code,
                "access_token": response["access_token"],
                "refresh_token": response["refresh_token"],
                "expires_in": response["expires_in"],
                "token_expiry": date_expiration,
                "status": "valid",
            }
        )
        return werkzeug.utils.redirect("/web", 303)
