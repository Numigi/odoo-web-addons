# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import json

from odoo.tests.common import HttpCase, tagged


@tagged('-at_install', 'post_install')
class TestAttachmentSizeLimit(HttpCase):

    def setUp(self):
        super().setUp()

        # 🔑 OBLIGATOIRE : démarre le serveur HTTP de test
        self.authenticate('admin', 'admin')

        # Limite faible pour les tests
        self.env['ir.config_parameter'].sudo().set_param(
            'web_attachment_size_limit.max_upload_size', '100'
        )

        self.user = self.env.user

    def _upload_file(self, content: bytes, filename='test.txt'):
        files = {
            'ufile': (filename, io.BytesIO(content), 'text/plain'),
        }
        data = {
            'model': 'res.users',
            'id': str(self.user.id),
        }

        return self.url_open(
            '/web/binary/upload_attachment',
            data=data,
            files=files,
        )

    def test_02_upload_too_large(self):
        file_content = b'x' * 200

        response = self._upload_file(
            file_content,
            filename='too_big.txt'
        )

        self.assertEqual(response.status_code, 413)

        payload = json.loads(response.text)
        self.assertIn('error', payload)

    def test_03_upload_success(self):
        file_content = b'x' * 50

        response = self._upload_file(
            file_content,
            filename='small_file.txt'
        )

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.text)
        self.assertIn('id', payload)

        attachment = self.env['ir.attachment'].browse(payload['id'])
        self.assertTrue(attachment.exists())
