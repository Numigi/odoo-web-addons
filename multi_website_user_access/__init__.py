# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models  # noqa: F401

from odoo import api, SUPERUSER_ID


def set_default_website(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    default_website = env.ref("website.default_website")
    default_website.write({"default_website": True})
    # Set default website for all existing users
    env["res.users"].search([]).write(
        {"allowed_website_ids": [(4, default_website.id)]}
    )
