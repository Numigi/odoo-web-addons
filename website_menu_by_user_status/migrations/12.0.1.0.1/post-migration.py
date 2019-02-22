# Copyright 2019 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def migrate(cr, version):
    """Propagate the user_logged/not_logged fields to dupplicate menu entries.

    In Odoo 12.0, multiple website is enabled.
    However, one website is defined as main website.
    Every menu entry in the main website is dupplicated:

    | Website      | URL          |
    |-----------------------------|
    | Your Company | /            |
    | Your Company | /aboutus     |
    | Your Company | /contact     |
    | <empty>      | /            |
    | <empty>      | /aboutus     |
    | <empty>      | /contact     |
    |--------------|--------------|

    When website is migrated, the dupplicate are created without the fields
    user_logged and user_not_logged.

    Therefore, they must be propagated from the original to the new menu entries.
    """
    env = Environment(cr, SUPERUSER_ID, {})
    menus_with_user_logged = env['website.menu'].search([('user_logged', '=', True)])
    for menu in menus_with_user_logged:
        dupplicate_menus = env['website.menu'].search([('url', '=', menu.url)])
        dupplicate_menus.write({'user_logged': True})

    menus_with_user_not_logged = env['website.menu'].search([('user_not_logged', '=', True)])
    for menu in menus_with_user_not_logged:
        dupplicate_menus = env['website.menu'].search([('url', '=', menu.url)])
        dupplicate_menus.write({'user_not_logged': True})
