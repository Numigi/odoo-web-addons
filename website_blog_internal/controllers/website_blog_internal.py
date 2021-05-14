# Copyright 2021 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from werkzeug.exceptions import NotFound


class WebsiteBlogInternal(WebsiteBlog):
    @http.route(
        [
            "/blog",
            "/blog/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def blogs(self, page=1, **post):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound("Page not found.")
        return super().blogs(page=page, **post)

    @http.route(
        [
            """/blog/<model("blog.blog", "[('website_id', 'in', (False, current_website_id))]"):blog>""",
            """/blog/<model("blog.blog"):blog>/page/<int:page>""",
            """/blog/<model("blog.blog"):blog>/tag/<string:tag>""",
            """/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>""",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def blog(self, blog=None, tag=None, page=1, **opt):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound("Page not found.")
        return super().blog(blog=blog, tag=tag, page=page, **opt)

    @http.route(
        [
            """/blog/<model("blog.blog", "[('website_id', 'in', (False, current_website_id))]"):blog>/feed"""
        ],
        type="http",
        auth="user",
        website=True,
    )
    def blog_feed(self, blog, limit="15", **kwargs):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound("Page not found.")
        return super().blog_feed(blog=blog, limit=limit, **kwargs)

    @http.route(
        [
            """/blog/<model("blog.blog", "[('website_id', 'in', (False, current_website_id))]"):blog>/post/<model("blog.post", "[('blog_id','=',blog[0])]"):blog_post>""",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def blog_post(
        self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post
    ):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound("Page not found.")
        return super().blog_feed(
            blog=blog,
            blog_post=blog_post,
            tag_id=tag_id,
            page=page,
            enable_editor=enable_editor,
            **post
        )
