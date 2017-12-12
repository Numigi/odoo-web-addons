/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('disable_quick_create', function(require) {
    "use strict";

    var core = require('web.core');
    var common = require('web.form_common');
    var Widget = require('web.Widget');
    var form_relational = require('web.form_relational');
    var data = require('web.data');
    var _t = core._t;
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

    var FieldMany2OneExtended = form_relational.FieldMany2One.extend(common.CompletionFieldMixin, {
        init: function(field_manager, node) {
            this._super(field_manager, node);

            this.options.no_quick_create = true;

            if (models.includes(this.field.relation)){
                this.options.no_create_edit = true;
            }
        },
    });

    var FieldMany2ManyTagsExtended = form_relational.FieldMany2ManyTags.extend(common.CompletionFieldMixin, {
        init: function(field_manager, node) {
            this._super(field_manager, node);
        },
        initialize_content: function() {
            if(!this.get("effective_readonly")) {
                // This line is added to use the new FieldManyOne structure
                this.many2one = new FieldMany2OneExtended(this.field_manager, this.node);
                this.many2one.options.no_open = true;
                this.many2one.on('changed_value', this, function() {
                    var newValue = this.many2one.get('value');
                    if(newValue) {
                        this.add_id(newValue);
                        this.many2one.set({'value': false});
                    }
                });

                this.many2one.prependTo(this.$el);

                var self = this;
                this.many2one.$('input').on('keydown', function(e) {
                    if(!$(e.target).val() && e.which === 8) {
                        var $badges = self.$('.badge');
                        if($badges.length) {
                            self.remove_id($badges.last().data('id'));
                        }
                    }
                });
                this.many2one.get_search_blacklist = function () {
                    return self.get('value');
                };
            }
        },
    });

    core.form_widget_registry.add('many2one', FieldMany2OneExtended)
                             .add('many2many_tags', FieldMany2ManyTagsExtended);

});
