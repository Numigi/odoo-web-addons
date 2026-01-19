# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import _, http
from odoo.http import request
from odoo.addons.web.controllers.main import Binary

class BinaryUploadLimit(Binary):

    @http.route('/web/binary/upload_attachment', type='http', auth="user")
    def upload_attachment(self, model, id, ufile, callback=None):
        """
        Override the upload_attachment method to enforce a server-side
        file size check based on the system parameter 'web.max_file_upload_size'.
        """
        # Retrieve the limit from System Parameters
        # Odoo standard default is often 128MB if not set.
        ICP = request.env['ir.config_parameter'].sudo()
        limit_str = ICP.get_param('web.max_file_upload_size')

        if limit_str:
            try:
                max_size = int(limit_str)
            except ValueError:
                # If the parameter is not a valid integer, we ignore the check
                # or log a warning. Here we just proceed to super.
                max_size = 0

            if max_size > 0:
                files = request.httprequest.files.getlist('ufile')
                for ufile_item in files:
                    # Check file size.
                    # seek(0, 2) moves the cursor to the end of the file to get the size
                    ufile_item.seek(0, 2)
                    file_size = ufile_item.tell()
                    # Reset cursor to the beginning for the actual read/save later
                    ufile_item.seek(0)

                    if file_size > max_size:
                        # Convert bytes to MB for the error message (rounded to 2 decimals)
                        limit_mb = round(max_size / 1024 / 1024, 2)
                        args = {'error': _("File too large. Global limit is %s MB.") % limit_mb}
                        return self._return_upload_error(callback, args)

        return super(BinaryUploadLimit, self).upload_attachment(model, id, ufile, callback=callback)

    def _return_upload_error(self, callback, args):
        """
        Format the error response for the Odoo web client.
        The web client expects a script trigger if a callback is provided (iframe upload).
        """
        if callback:
            return """<script>window.top.window.jQuery(window.top.window).trigger('%s', %s);</script>""" % (callback, json.dumps(args))
        return json.dumps(args)