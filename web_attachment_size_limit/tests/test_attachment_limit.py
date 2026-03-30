# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import json

from odoo.tests.common import HttpCase, tagged


@tagged("-at_install", "post_install")
class TestAttachmentSizeLimit(HttpCase):

    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].sudo().set_param(
            "web_attachment_size_limit.max_upload_size", "100"
        )

    def _upload_file(self, content: bytes, filename="test.txt"):
        files = {"ufile": (filename, io.BytesIO(content), "text/plain")}
        data = {"model": "res.users", "id": str(self.env.user.id)}
        return self.url_open("/web/binary/upload_attachment", data=data, files=files)

    def test_02_upload_too_large(self):
        response = self._upload_file(b"x" * 200, filename="too_big.txt")
        assert response.status_code == 200
        assert "File too large" in response.text

    def test_03_upload_success(self):
        response = self._upload_file(b"x" * 50, filename="small_file.txt")
        assert response.status_code == 200
        payload = json.loads(response.text)
        assert "id" in payload
        assert self.env["ir.attachment"].browse(payload["id"]).exists()