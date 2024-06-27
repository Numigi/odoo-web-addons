# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models

from odoo import api, SUPERUSER_ID


def set_default_website(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    default_website = env.ref("website.default_website")
    default_website.write({"default_website": True})
    # Set default website for all existing users
    internal_users = (
        env["res.users"].with_context(active_test=False).search([("share", "=", False)])
    )
    external_users = (
        env["res.users"].with_context(active_test=False).search([("share", "=", True)])
    )
    internal_users.write({"website_ids": [(6, 0, env["website"].search([]).ids)]})
    external_users.write({"website_ids": [(4, default_website.id)]})
