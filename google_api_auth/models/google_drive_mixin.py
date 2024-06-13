# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import fields, models, _
import google_auth_oauthlib.flow
from werkzeug.urls import url_join
from odoo.exceptions import UserError
import requests
from ..controllers.main import GOOGLE_TOKEN_ENDPOINT
from datetime import timedelta

_logger = logging.getLogger(__name__)


class GoogleDriveMixin(models.AbstractModel):
    _name = "google.drive.mixin"
    _description = "Google Drive Mixin"

    active = fields.Boolean(string="Active", default=True, groups="base.group_system")
    name = fields.Char(
        string="Application name", required=True, groups="base.group_system", copy=False
    )
    auth_uri = fields.Char(string="Auth URI", groups="base.group_system")
    auth_provider_x509_cert_url = fields.Char(
        string="Auth Provider x509 Cert URL", groups="base.group_system"
    )
    client_id = fields.Char(
        string="Client ID", required=True, groups="base.group_system", copy=False
    )
    client_secret = fields.Char(
        string="Client Secret", required=True, groups="base.group_system", copy=False
    )
    code = fields.Char(string="Code", groups="base.group_system", copy=False)
    expires_in = fields.Integer(string="Expires in", groups="base.group_system")
    redirect_uri_ids = fields.One2many(
        "google.redirect.uri",
        "google_application_id",
        string="Redirect URIs",
        groups="base.group_system",
    )
    refresh_token = fields.Char(
        string="Refresh Token", groups="base.group_system", copy=False
    )
    scope_ids = fields.One2many(
        "google.application.scope",
        "google_application_id",
        string="Scopes",
        groups="base.group_system",
    )
    access_token = fields.Char(string="Token", groups="base.group_system", copy=False)
    token_expiry = fields.Datetime(string="Token Expiry", groups="base.group_system")
    token_uri = fields.Char(string="Token URI", groups="base.group_system")
    status = fields.Selection(
        [
            ("valid", "Valid"),
            ("invalid", "Invalid"),
        ],
        string="Status",
        default="invalid",
        groups="base.group_system",
    )

    def button_refresh_token(self):
        self.ensure_one()

        if not self.access_token:
            self.refresh_token = False
            self.access_token = False
            self.expires_in = False
            self.token_expiry = False
            scopes = [" ".join(self.scope_ids.mapped("name"))]
            client_config = {
                "web": {
                    "client_id": self.client_id,
                    "project_id": self.name,
                    "auth_uri": self.auth_uri,
                    "token_uri": self.token_uri,
                    "client_secret": self.client_secret,
                    "auth_provider_x509_cert_url": self.auth_provider_x509_cert_url,
                    "redirect_uris": [
                        redirect_uri.name for redirect_uri in self.redirect_uri_ids
                    ],
                }
            }
            base_url = self.get_base_url()
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config, scopes
            )
            flow.redirect_uri = url_join(base_url, "/google_account/authentification")

            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
                login_hint="hint@example.com",
                prompt="consent",
            )

            return {
                "type": "ir.actions.act_url",
                "url": authorization_url,
            }

        elif (
            self.access_token
            and self.token_expiry
            and self.token_expiry < datetime.now()
        ):
            req = self.refresh_access_token()
            response = req.json()

            if req.status_code != 200:
                _logger.error(
                    "Google Application: Error %s when refreshing token.",
                    req.status_code,
                )
                self.write({"status": "invalid"})

            date_expiration = datetime.now() + timedelta(seconds=response["expires_in"])

            self.write(
                {
                    "access_token": response["access_token"],
                    "expires_in": response["expires_in"],
                    "token_expiry": date_expiration,
                    "status": "valid",
                }
            )

        else:
            raise UserError(_("The access token is still valid."))

    def refresh_access_token(self):
        self.ensure_one()
        headers = {
            "Host": "oauth2.googleapis.com",
            "Content-type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "access_type": "offline",
            "refresh_token": self.refresh_token,
        }
        req = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, headers=headers)
        return req
