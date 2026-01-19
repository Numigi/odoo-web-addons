# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import json
from odoo.tests.common import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestAttachmentSizeLimit(HttpCase):

    def setUp(self):
        super(TestAttachmentSizeLimit, self).setUp()
        # Authenticate as admin to have upload rights and establish session
        self.authenticate('admin', 'admin')

        # Force the parameter value for the test context (e.g., 100 bytes)
        self.env['ir.config_parameter'].sudo().set_param(
            'web.max_file_upload_size', '100'
        )

    def _get_csrf_token(self):
        """
        Fetch the CSRF token from the session info.
        This is required for controllers protected by
        @http.route(..., csrf=True)
        """
        # We invoke get_session_info via JSON-RPC to retrieve the token
        # url_open does not support 'json' param, so we serialize manually
        response = self.url_open(
            '/web/session/get_session_info',
            data=json.dumps({}),
            headers={'Content-Type': 'application/json'}
        )
        return response.json().get('result', {}).get('csrf_token')

    def test_01_parameter_exists(self):
        """Check that the system parameter is correctly set."""
        param = self.env['ir.config_parameter'].sudo().get_param(
            'web.max_file_upload_size'
        )
        self.assertEqual(
            param, '100', "The parameter value should be 100 for this test."
        )

    def test_02_upload_too_large(self):
        """Try to upload a file of 200 bytes (limit is 100). Should fail."""

        csrf_token = self._get_csrf_token()

        file_content = b'x' * 200
        files = {
            'ufile': ('big_file.txt', io.BytesIO(file_content), 'text/plain'),
        }
        # We must send the model/id and CSRF token as data fields
        data = {
            'model': 'res.users',
            'id': str(self.env.user.id),
            'csrf_token': csrf_token
        }

        # Note: /web/binary/upload_attachment is the standard upload URL
        response = self.url_open(
            '/web/binary/upload_attachment', data=data, files=files
        )

        response_content = response.content.decode('utf-8')

        self.assertIn(
            "File too large",
            response_content,
            "The upload should have been blocked with an error message. "
            "Response: %s" % response_content
        )

    def test_03_upload_success(self):
        """Try to upload a file of 50 bytes (limit is 100). Should succeed."""

        csrf_token = self._get_csrf_token()

        file_content = b'x' * 50
        files = {
            'ufile': (
                'small_file.txt', io.BytesIO(file_content), 'text/plain'
            ),
        }
        data = {
            'model': 'res.users',
            'id': str(self.env.user.id),
            'csrf_token': csrf_token
        }

        response = self.url_open(
            '/web/binary/upload_attachment', data=data, files=files
        )
        response_content = response.content.decode('utf-8')

        self.assertNotIn(
            "error", response_content,
            "Valid upload should not return an error."
        )
        self.assertIn(
            "small_file.txt", response_content,
            "The filename should be in the response."
        )
