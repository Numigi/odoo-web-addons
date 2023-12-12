# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
from odoo.tests.common import TransactionCase
from odoo.tools.misc import file_open
from odoo import http


class FakeRequest(object):
    def __init__(self, env):
        self.env = env

    def make_response(self, data, headers):
        return FakeResponse(data, headers)


class FakeResponse(object):
    def __init__(self, data, headers):
        self.data = data
        self.headers = dict(headers)


class TestWebFavicon(TransactionCase):
    def test_web_favicon(self):
        original_request = http.request
        http.request = FakeRequest(self.env)
        from ..controllers.web_favicon import WebFavicon

        company = self.env["res.company"].search([], limit=1)
        # default icon
        company.write(
            {
                "favicon": False,
            }
        )
        data = WebFavicon().icon()
        self.assertEqual(data.headers["Content-Type"], "image/x-icon")
        # our own icon
        company.write(
            {
                "favicon": base64.b64encode(
                    file_open(
                        "web_favicon/static/description/image_test.ico", "rb"
                    ).read()
                ),
            }
        )
        data = WebFavicon().icon()
        self.assertEqual(data.headers["Content-Type"], "image/x-icon")
        http.request = original_request
