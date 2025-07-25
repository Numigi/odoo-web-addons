/*
    © Numigi (tm) and all its contributors (https://numigi.com/r/home)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_form_disable_autocomplete.input_field", function(require) {
"use strict";

var InputField = require("web.basic_fields").InputField;

InputField.include({
    _prepareInput() {
        var res = this._super.apply(this, arguments);
        this.$input.attr({"autocomplete": "off"});
        return res;
    },
});

});
