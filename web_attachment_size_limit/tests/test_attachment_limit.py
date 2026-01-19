# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
from odoo.tests.common import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestAttachmentSizeLimit(HttpCase):

    def setUp(self):
        super(TestAttachmentSizeLimit, self).setUp()
        # Authenticate as admin to have upload rights
        self.authenticate('admin', 'admin')

        # Force the parameter value for the test context (e.g., 100 bytes)
        # This prevents the test from depending on the default configuration
        self.env['ir.config_parameter'].sudo().set_param(
            'web.max_file_upload_size', '100'
        )

    def test_01_parameter_exists(self):
        """Check that the system parameter is correctly set."""
        param = self.env['ir.config_parameter'].sudo().get_param('web.max_file_upload_size')
        self.assertTrue(param, "The parameter web.max_file_upload_size should exist.")
        self.assertEqual(param, '100', "The parameter value should be 100 for this test.")

    def test_02_upload_too_large(self):
        """Try to upload a file of 200 bytes (limit is 100). Should fail."""

        # Create a dummy file content of 200 bytes ('x' * 200)
        file_content = b'x' * 200
        files = {
            'ufile': ('big_file.txt', io.BytesIO(file_content), 'text/plain'),
            'model': (None, 'res.users'),
            'id': (None, str(self.env.user.id)),
        }

        # Simulate the controller call via url_open (acting as a browser)
        # Note: /web/binary/upload_attachment is the standard upload URL
        response = self.url_open('/web/binary/upload_attachment', files=files)

        # The controller returns JSON (sometimes wrapped in an HTML script tag)
        # We verify if the error message defined in main.py is present
        response_content = response.content.decode('utf-8')

        self.assertIn(
            "File too large",
            response_content,
            "The upload should have been blocked with an error message."
        )

    def test_03_upload_success(self):
        """Try to upload a file of 50 bytes (limit is 100). Should succeed."""

        file_content = b'x' * 50
        files = {
            'ufile': ('small_file.txt', io.BytesIO(file_content), 'text/plain'),
            'model': (None, 'res.users'),
            'id': (None, str(self.env.user.id)),
        }

        response = self.url_open('/web/binary/upload_attachment', files=files)
        response_content = response.content.decode('utf-8')

        # In case of success, Odoo does not return an 'error' key, but file info
        self.assertNotIn("error", response_content, "Valid upload should not return an error.")
        self.assertIn("small_file.txt", response_content, "The filename should be in the response.")