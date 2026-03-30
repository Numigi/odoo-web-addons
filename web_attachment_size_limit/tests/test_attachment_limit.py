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
        ufile_mock.tell.return_value = content_length

        patch_req = patch("odoo.addons.web_attachment_size_limit.controllers.main.request")
        patch_sup = patch("odoo.addons.web.controllers.main.Binary.upload_attachment")

        with patch_req as mock_req, patch_sup as mock_sup:
            mock_req.env = self.env
            mock_req.httprequest.files.getlist.return_value = [ufile_mock]
            mock_sup.return_value = '{"id": 123}'

            res = self.controller.upload_attachment(
                model="res.users",
                id=self.env.user.id,
                ufile=ufile_mock,
            )
            return res, mock_sup.called

    def test_02_upload_too_large(self):
        response, super_called = self._test_upload(200)
        assert "File too large" in response
        assert not super_called

    def test_03_upload_success(self):
        response, super_called = self._test_upload(50)
        assert response == '{"id": 123}'
        assert super_called