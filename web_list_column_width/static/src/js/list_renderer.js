/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)

    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_list_column_width.list_renderer", function(require) {
"use strict";

require("web.ListRenderer").include({
    /**
     * Set the width on the column header.
     */
    _renderHeaderCell(node) {
        var th = this._super.apply(this, arguments);
        if(node.attrs.width){
            th = th.css("width", node.attrs.width);
        }
        return th;
    },
});
});
