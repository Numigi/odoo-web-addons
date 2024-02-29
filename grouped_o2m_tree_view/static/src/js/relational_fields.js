odoo.define('smile_grouped_o2m_tree_view.relational_fields', function (require) {
    "use strict";

    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var relational_fields = require('web.relational_fields');
    var ListRenderer = require('web.ListRenderer');

    var _t = core._t;

    var List_renderer = ListRenderer.extend({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.group_by = params.group_by;
            this.group_by_field_type = state.data[0].fields[this.group_by].type;
            this.new_sorted_data = [];
            this.grouped_records = this._groupRecords(state.data);
        },
        _groupRecords: function (data) {
            var self = this;
            return _.groupBy(data, function (row) {
                var group_by_field = row.data[self.group_by];
                if (group_by_field) {
                    return (self.group_by_field_type === 'many2one') ?
                        group_by_field.data.display_name :
                        group_by_field;
                } else {
                    return false;
                }
            });
        },

        _renderBody: function () {
            var self = this;
            var $body = $('<tbody>');
            var data_index = 0;

            _.each(this.grouped_records, function (group) {
                _.each(group, function (rec) {
                    self.new_sorted_data.push(rec);
                });
                var group_by_string;
                if (group[0].data[self.group_by]) {
                    // if group_by_field_value is set.
                    group_by_string = group[0].data[self.group_by];
                    // if group by field is m2o, the group_by_field_value is retrieved from data.display_name.
                    // if not data.display_name raises 'undefined' error.
                    if (self.group_by_field_type === 'many2one') {
                        group_by_string = group[0].data[self.group_by].data.display_name;
                    }
                    var $tr = self._renderGroupTitle(group_by_string, group);
                    $body.append($tr);
                    _.each(self.state.data, function (record) {
                        if (self.group_by_field_type === 'many2one') {
                            if (record.data[self.group_by] && record.data[self.group_by].data.display_name == group_by_string) {
                                $body.append(self._renderRow(record));
                            }
                        }
                        else {
                            if (record.data[self.group_by] && record.data[self.group_by] == group_by_string) {
                                $body.append(self._renderRow(record));
                            }
                        }
                    });
                } else {
                    // if group_by_field_value  is false.
                    group_by_string = 'False';
                    var $tr = self._renderGroupTitle(group_by_string, group);
                    $body.append($tr);
                    _.each(self.state.data, function (record) {
                        if (!record.data[self.group_by]) {
                            $body.append(self._renderRow(record));
                        }
                    });
                }
            });
            this.state.data = this.new_sorted_data;

            // Add 'Add an item' button when view is not readonly.
            this._addAddItemButton($body);

            return $body;

        },

        _addAddItemButton: function ($body) {
            if (this.addCreateLine) {
                var $a = $('<a href="#">').text(_t("Add an item"));
                var $td = $('<td>').attr('colspan', this._getNumberOfCols())
                    .addClass('o_field_x2many_list_row_add')
                    .append($a);
                var $tr = $('<tr>').append($td);
                $body.append($tr);
            }
        },

        _calculateSum: function (group) {
            var sum = 0;
            _.each(group, function (rec) {
                sum += rec.data['price_subtotal'];
            });
            return sum;
        },

        _renderGroupTitle: function (name, group) {
            var sum = this._calculateSum(group);
            var $th_name = $('<th/>', { class: 'o_group_name' }).attr('colspan', this._getNumberOfCols() - 1);
            $th_name.append($('<span>').text(name));
            var $th_price = $('<th/>', { class: 'o_group_subtotal o_list_number' });
            $th_price.append($('<span>').text(sum.toFixed(2)));
            var $th = $th_name.add($th_price);
            var $tr = $('<tr/>', { class: 'o_group_header o_group_has_content' }).append($th);
            return $tr;
        },

        _onToggleGroup: function () {
            return null;
        },
    });


    var WidgetGroupByX2ManyList = relational_fields.FieldOne2Many.extend({

        init: function () {
            this._super.apply(this, arguments);
        },

        _render: function () {
            if (!this.attrs.group_by || this.record.data[this.attrs.name].data.length === 0) {
                return this._super();
            }

            var viewType = 'list';
            this.currentColInvisibleFields = this._evalColumnInvisibleFields();
            this.renderer = new List_renderer(this, this.value, {
                group_by: this.attrs.group_by,
                arch: this.view.arch,
                editable: this.mode === 'edit' && this.view.arch.attrs.editable,
                addCreateLine: !this.isReadonly && this.activeActions.create,
                addTrashIcon: !this.isReadonly && this.activeActions.delete,
                viewType: viewType,
                columnInvisibleFields: this.currentColInvisibleFields,
            });
            this.$el.empty();
            return this.renderer.appendTo(this.$el);
        },

    });


    field_registry.add('grouped_o2many_tree', WidgetGroupByX2ManyList);

    return {
        WidgetGroupByX2ManyList: WidgetGroupByX2ManyList,
    };
});