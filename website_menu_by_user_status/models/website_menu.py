# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2018 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WebsiteMenu(models.Model):

    _inherit = 'website.menu'

    user_logged = fields.Boolean(
        string="User Logged",
        default=True,
        help="If checked, the menu will be displayed when the user is logged."
    )

    user_not_logged = fields.Boolean(
        string="User Not Logged",
        default=True,
        help="If checked, the menu will be displayed "
             "when the user is not logged."
    )

    group_ids = fields.Many2many(
        'res.groups', 'website_menu_group_rel', 'menu_id', 'group_id', 'Group',
        help="If filled, the menu item is only visible to the users "
        "from one of the selected groups."
    )

    def _compute_visible(self):
        super()._compute_visible()

        public_user = self.env.ref('base.public_user')

        for menu in self:
            if menu.env.user == public_user:
                menu.is_visible = menu.is_visible and menu.user_not_logged
            else:
                menu.is_visible = menu.is_visible and menu.user_logged
