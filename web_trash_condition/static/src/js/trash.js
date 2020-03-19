/*
    © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_trash_condition", function(require) {
"use strict";

const trashInvisibleField = "trash_widget_invisible";

// The editable list properties must be included before
// so that the method _renderRow can be overrided properly.
require("web.EditableListRenderer")

require("web.ListRenderer").include({
    _renderRow(record) {
        var $row = this._super.apply(this, arguments);

        if(this._isTrashInvisible(record)){
            this._hideTrashFromRow($row);
        }

        return $row
    },

    _isTrashInvisible(record) {
        return Boolean(record.data[trashInvisibleField]);
    },

    _hideTrashFromRow($row) {
        $row.find('.o_list_record_remove button').addClass("d-none");
        $row.find('.o_list_record_remove').removeClass("o_list_record_remove");
    },
});
});
