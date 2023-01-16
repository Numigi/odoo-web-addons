# Copyright 2023 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from werkzeug.exceptions import NotFound


class WebsiteBlogInternal(WebsiteBlog):

    @http.route(
        [
            '/blog',
            '/blog/page/<int:page>',
            '/blog/tag/<string:tag>',
            '/blog/tag/<string:tag>/page/<int:page>',
            '''/blog/<model("blog.blog"):blog>''',
            '''/blog/<model("blog.blog"):blog>/page/<int:page>''',
            '''/blog/<model("blog.blog"):blog>/tag/<string:tag>''',
            '''/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>'''
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=True
    )
    def blog(self, blog=None, tag=None, page=1, search=None, **opt):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound()
        return super(WebsiteBlogInternal, self).blog(blog=blog, tag=tag, page=page, **opt)

    @http.route(['''/blog/<model("blog.blog"):blog>/feed'''], type='http', auth="public", website=True, sitemap=True)
    def blog_feed(self, blog, limit="15", **kwargs):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound()
        return super(WebsiteBlogInternal, self).blog_feed(blog=blog, limit=limit, **kwargs)

    @http.route([
        '''/blog/<model("blog.blog"):blog>/<model("blog.post", "[('blog_id','=',blog.id)]"):blog_post>''',
    ], type='http', auth="public", website=True, sitemap=True)
    def blog_post(
            self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post
    ):
        if not http.request.env.user.has_group("base.group_user"):
            raise NotFound()
        return super(WebsiteBlogInternal, self).blog_post(
            blog=blog,
            blog_post=blog_post,
            tag_id=tag_id,
            page=page,
            enable_editor=enable_editor,
            **post
        )
