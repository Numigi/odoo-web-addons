/*
    © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_handle_condition", function(require) {
"use strict";

const basicFields = require("web.basic_fields");
const handleInvisibleField = "handle_widget_invisible";

basicFields.HandleWidget.include({
    _render() {
        this._super.apply(this, arguments);

        if(this._isHandleInvisible()){
            this._hideHandle();
        }
    },

    _reset() {
        this._super.apply(this, arguments);

        if(this._isHandleInvisible()){
            this._hideHandle();
        }
        else {
            this._showHandle();
        }
    },

    _isHandleInvisible() {
        return Boolean(this.record.data[handleInvisibleField]);
    },

    _hideHandle() {
        this.$el.addClass("d-none");
    },

    _showHandle() {
        this.$el.removeClass("d-none");
    },
});
});
