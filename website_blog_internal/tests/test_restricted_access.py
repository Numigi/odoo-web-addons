# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.tests import SavepointCase
from ..controllers.website_blog_internal import WebsiteBlogInternal
from werkzeug.exceptions import NotFound
from odoo.addons.test_http_request.common import mock_odoo_request


class TestWebsiteMenu(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env.ref("base.user_demo")
        cls.customer = cls.env.ref("base.demo_user0")
        cls.blog = cls.env["blog.blog"].search([], limit=1)

    def test_employee_access(self):
        with mock_odoo_request(self.env(user=self.employee)):
            WebsiteBlogInternal().blogs()

    def test_customer_access(self):
        with mock_odoo_request(self.env(user=self.customer)), pytest.raises(NotFound):
            WebsiteBlogInternal().blogs()

    def test_employee_access_page(self):
        with mock_odoo_request(self.env(user=self.employee)):
            WebsiteBlogInternal().blog(blog=self.blog)

    def test_customer_access_page(self):
        with mock_odoo_request(self.env(user=self.customer)), pytest.raises(NotFound):
            WebsiteBlogInternal().blog(blog=self.blog)

    def test_employee_access_feed(self):
        with mock_odoo_request(self.env(user=self.employee)):
            WebsiteBlogInternal().blog_feed(blog=self.blog)

    def test_customer_access_feed(self):
        with mock_odoo_request(self.env(user=self.customer)), pytest.raises(NotFound):
            WebsiteBlogInternal().blog_feed(blog=self.blog)

    def test_employee_access_post(self):
        with mock_odoo_request(self.env(user=self.employee)):
            WebsiteBlogInternal().blog_post(
                blog=self.blog, blog_post=self.env["blog.post"].search([], limit=1)
            )

    def test_customer_access_post(self):
        with mock_odoo_request(self.env(user=self.customer)), pytest.raises(NotFound):
            WebsiteBlogInternal().blog_post(
                blog=self.blog, blog_post=self.env["blog.post"].search([], limit=1)
            )
