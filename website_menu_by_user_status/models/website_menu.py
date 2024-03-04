# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2018 Numigi
# Copyright 2023 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """

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

    def _compute_visible(self):
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()

        for menu in self:
            if not menu.is_visible:
                return

            if self.env.user == self.env.ref('base.public_user'):
                menu.is_visible = menu.user_not_logged
            else:
                menu.is_visible = menu.user_logged


class WebsiteMenuVisibleForSpecificGroups(models.Model):
    """Optionally display the menu item for a given list of user groups."""

    _inherit = 'website.menu'

    group_ids = fields.Many2many(
        'res.groups', 'website_menu_group_rel', 'menu_id', 'group_id', 'Group',
        help="If filled, the menu item is only visible to the users "
        "from one of the selected groups."
    )

    def _compute_visible(self):
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()
        for menu in self:
            if not menu.is_visible:
                return

            if menu.group_ids:
                user_has_any_group = bool(self.env.user.groups_id & menu.group_ids)
                menu.is_visible = user_has_any_group
