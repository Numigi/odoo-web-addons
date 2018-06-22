# Copyright 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class BaseConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    google_attachment_client_id = fields.Char(
        'Google OAuth2 Client Id',
        default=lambda s: s.env['ir.config_parameter'].get_param('google_attachment.client_id'))

    google_attachment_api_key = fields.Char(
        'Google Api Key',
        default=lambda s: s.env['ir.config_parameter'].get_param('google_attachment.api_key'))

    def set_values(self):
        super().set_values()

        icp = self.env['ir.config_parameter']
        icp.set_param('google_attachment.client_id', self.google_attachment_client_id)

        icp = self.env['ir.config_parameter']
        icp.set_param('google_attachment.api_key', self.google_attachment_api_key)
