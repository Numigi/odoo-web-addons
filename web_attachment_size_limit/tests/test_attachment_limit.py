# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import json

from odoo.tests.common import HttpCase, tagged


@tagged('-at_install', 'post_install')
class TestAttachmentSizeLimit(HttpCase):
    """Tests HTTP for web_attachment_size_limit"""

    def setUp(self):
        super().setUp()

        # Définir une limite faible pour les tests (100 bytes)
        self.env['ir.config_parameter'].sudo().set_param(
            'web_attachment_size_limit.max_upload_size', '100'
        )

        self.user = self.env.user

    def _upload_file(self, content: bytes, filename='test.txt'):
        """Helper pour uploader un fichier via le contrôleur web"""
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
        """Upload > limite (200 bytes). Doit échouer."""
        file_content = b'x' * 200

        response = self._upload_file(
            file_content,
            filename='too_big.txt'
        )

        self.assertEqual(
            response.status_code, 413,
            'Upload should be rejected with HTTP 413'
        )

        payload = json.loads(response.text)
        self.assertIn('error', payload)
        self.assertIn('exceed', payload['error'].lower())

    def test_03_upload_success(self):
        """Upload < limite (50 bytes). Doit réussir."""
        file_content = b'x' * 50

        response = self._upload_file(
            file_content,
            filename='small_file.txt'
        )

        self.assertEqual(
            response.status_code, 200,
            'Upload should succeed'
        )

        payload = json.loads(response.text)
        self.assertIn('id', payload)

        attachment = self.env['ir.attachment'].browse(payload['id'])
        self.assertTrue(attachment.exists())
        self.assertEqual(attachment.res_model, 'res.users')
        self.assertEqual(attachment.res_id, self.user.id)
