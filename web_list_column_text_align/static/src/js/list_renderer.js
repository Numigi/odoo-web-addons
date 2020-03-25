/*
    © 2020 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_list_column_text_align.list_renderer", function(require) {
"use strict";

require("web.ListRenderer").include({
    /**
     * Set the width on the column header.
     */
    _renderHeaderCell(node) {
        var th = this._super.apply(this, arguments);
        if(node.attrs.align){
            th = th.css("text-align", node.attrs.align);

        }
        return th;
    },
});
});
