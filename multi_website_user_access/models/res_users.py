# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    def _get_default_website(self):
        return self.env["website"].search([("default_website", "=", True)])

    allowed_website_ids = fields.Many2many(
        "website",
        default=_get_default_website,
        string="Allowed Websites",
        store=True,
        readonly=False,
        help="Restrict user access to specific websites.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        user_groups, grp_portal, grp_public = self._get_user_groups()
        for vals in vals_list:
            self._assign_portal_public_user(vals, user_groups, grp_portal, grp_public)
        users = super(Users, self).create(vals_list)
        return users

    def write(self, vals):
        user_groups, grp_portal, grp_public = self._get_user_groups()
        self._assign_portal_public_user(vals, user_groups, grp_portal, grp_public)
        return super(Users, self).write(vals)

    def _assign_portal_public_user(self, vals, user_groups, grp_portal, grp_public):
        if user_groups in vals:
            if vals.get(user_groups) in [grp_portal, grp_public]:
                default_website = self.env["website"].search(
                    [("default_website", "=", True)]
                )
                website_commands = [(4, website.id) for website in default_website]
                if vals.get("allowed_website_ids"):
                    vals["allowed_website_ids"] = (
                        website_commands + vals["allowed_website_ids"]
                    )
                else:
                    vals["allowed_website_ids"] = website_commands
        return vals

    def _get_user_groups(self):
        grp_internal = self.env.ref("base.group_user")
        grp_portal = self.env.ref("base.group_portal")
        grp_public = self.env.ref("base.group_public")
        user_groups = "sel_groups_%s_%s_%s" % (
            grp_internal.id,
            grp_portal.id,
            grp_public.id,
        )
        return user_groups, grp_portal.id, grp_public.id
