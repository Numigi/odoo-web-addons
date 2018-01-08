/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('disable_quick_create', function(require) {
    "use strict";

    var form_relational = require('web.form_relational');
    var Model = require('web.DataModel');

    var model_deferred = $.Deferred();
    var models = [];

    new Model('ir.model').call('search_read', [[['disable_create_edit','=', true]], ['model'],]).then(
        function(result) {
            result.forEach(function(el){
                models.push(el.model);
            })
            model_deferred.resolve();
        });

    form_relational.FieldMany2One.include({
        init: function(field_manager, node) {
            this._super(field_manager, node);

            this.options.no_quick_create = true;

            if (models.includes(this.field.relation)){
                this.options.no_create_edit = true;
            }
        },
    });
});
