# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """
    This hook is executed after the module installation.
    It sets the default upload limit ONLY if the parameter usually
    doesn't exist yet.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Check if the parameter already exists
    # We use get_param which returns False if not found
    current_value = env['ir.config_parameter'].get_param('web.max_file_upload_size')

    if not current_value:
        # 10 MB = 10485760 bytes
        env['ir.config_parameter'].set_param('web.max_file_upload_size', '10485760')
