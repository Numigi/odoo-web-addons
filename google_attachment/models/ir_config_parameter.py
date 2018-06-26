# Copyright 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class IrConfigParameterWithGoogleAttachmentParameters(models.Model):
    """Add a method to allow base users to fetch the google client id and api key.

    These 2 parameters are required on the client side for the Google Picker widget.
    """

    _inherit = 'ir.config_parameter'

    @api.model
    def get_google_attachment_parameters(self):
        return {
            'clientId': self.sudo().get_param('google_attachment.client_id'),
            'apiKey': self.sudo().get_param('google_attachment.api_key'),
        }
