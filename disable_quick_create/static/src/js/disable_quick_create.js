/*
    © 2017-2018 Savoir-faire Linux <https://savoirfairelinux.com>
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("disable_quick_create", function(require) {
    "use strict";

    var relationalFields = require("web.relational_fields");
    var rpc = require("web.rpc");

    var models = [];

    rpc.query({
        model: "ir.model",
        method: "search_read",
        args:[
            [["disable_create_edit", "=", true]],
            ["model"],
        ],
    }).then(function(result) {
        result.forEach(function(el){
            models.push(el.model);
        })
    });

    relationalFields.FieldMany2One.include({
        init() {
            this._super.apply(this, arguments);

            this.nodeOptions.no_quick_create = true;

            if (models.includes(this.field.relation)){
                this.nodeOptions.no_create = true;
                this.nodeOptions.no_create_edit = true;
                this.can_create = false;
            }
        },
    });
});
