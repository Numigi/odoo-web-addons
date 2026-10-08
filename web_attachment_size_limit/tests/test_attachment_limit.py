# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.tests.common import TransactionCase, tagged
from odoo.addons.web_attachment_size_limit.controllers.main import BinaryUploadLimit


@tagged("-at_install", "post_install")
class TestAttachmentSizeLimit(TransactionCase):

    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].sudo().set_param(
            "web.max_file_upload_size", "100"
        )
        self.controller = BinaryUploadLimit()

    def _test_upload(self, content_length: int):
        ufile_mock = MagicMock()

        # Simulate file behavior: after seek(0, 2), tell() returns file size
        position = [0]

        def mock_seek(offset, whence=0):
            if whence == 2:  # SEEK_END
                position[0] = content_length
            elif whence == 0:  # SEEK_SET
                position[0] = offset
            elif whence == 1:  # SEEK_CUR
                position[0] += offset

        def mock_tell():
            return position[0]

        ufile_mock.seek = mock_seek
        ufile_mock.tell = mock_tell

        # Create mock request object in advance to avoid inspecting LocalProxy
        mock_req = MagicMock()
        mock_req.env = self.env
        mock_req.httprequest.files.getlist.return_value = [ufile_mock]
        mock_req.endpoint = None  # Avoid Response trying to access endpoint.routing

        patch_req = patch(
            "odoo.addons.web_attachment_size_limit.controllers.main.request",
            new=mock_req
        )
        patch_sup = patch("odoo.addons.web.controllers.main.Binary.upload_attachment")

        with patch_req, patch_sup as mock_sup:
            mock_sup.return_value = '{"id": 123}'

            res = self.controller.upload_attachment(
                model="res.users",
                id=self.env.user.id,
                ufile=ufile_mock,
            )
            return res, mock_sup.called

    def test_02_upload_too_large(self):
        response, super_called = self._test_upload(200)
        self.assertIn("File too large", response)
        self.assertFalse(super_called)

    def test_03_upload_success(self):
        response, super_called = self._test_upload(50)
        self.assertEqual(response, '{"id": 123}')
        self.assertTrue(super_called)