# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
from odoo import http
from odoo.tests.common import HttpCase, tagged


@tagged('post_install', '-at_install', 'http_test')
class TestAttachmentSizeLimit(HttpCase):

    def setUp(self):
        super(TestAttachmentSizeLimit, self).setUp()
        self.authenticate('admin', 'admin')
        self.env['ir.config_parameter'].sudo().set_param(
            'web.max_file_upload_size', '100'
        )
        # On récupère l'URL de base pour url_open
        self.base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    def test_02_upload_too_large(self):
        """Try to upload a file of 200 bytes (limit is 100). Should fail."""

        # Utilisation de la méthode native pour le jeton CSRF
        csrf_token = http.WebRequest.csrf_token(self)

        file_content = b'x' * 200
        files = {
            'ufile': ('big_file.txt', io.BytesIO(file_content), 'text/plain'),
        }
        data = {
            'model': 'res.users',
            'id': str(self.env.user.id),
            'csrf_token': csrf_token
        }

        # Utilisation de l'URL complète avec la base_url
        response = self.url_open(
            url='%s/web/binary/upload_attachment' % self.base_url,
            data=data,
            files=files
        )

        self.assertIn("File too large", response.text)

    def test_03_upload_success(self):
        """Try to upload a file of 50 bytes (limit is 100). Should succeed."""

        csrf_token = http.WebRequest.csrf_token(self)

        file_content = b'x' * 50
        files = {
            'ufile': ('small_file.txt', io.BytesIO(file_content), 'text/plain'),
        }
        data = {
            'model': 'res.users',
            'id': str(self.env.user.id),
            'csrf_token': csrf_token
        }

        response = self.url_open(
            url='%s/web/binary/upload_attachment' % self.base_url,
            data=data,
            files=files
        )

        self.assertNotIn("error", response.text)
        self.assertIn("small_file.txt", response.text)
