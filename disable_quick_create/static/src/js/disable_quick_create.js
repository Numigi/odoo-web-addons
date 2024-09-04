/** @odoo-module **/

import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';

const originalLoadOptionsSource = Many2XAutocomplete.prototype.loadOptionsSource;

patch(Many2XAutocomplete.prototype, 'disable_quick_create.Many2XAutocomplete', {
    setup() {
        this._super(...arguments);
    },

    async isCreateDisabled() {
        var domain = [
            ['model', '=', this.props.resModel],
            ['disable_create_edit', '=', true],
        ];
        try {
            var result = await rpc.query({
                model: 'ir.model',
                method: 'search',
                args: [domain],
            });
            return result.length > 0;
        } catch (error) {
            console.error('Error in isCreateDisabled:', error);
            return false;
        }
    },

    async loadOptionsSource() {
        var isCreateDisabled = await this.isCreateDisabled();
        if (isCreateDisabled) {
            this.props.quickCreate = false;
            this.activeActions.createEdit = false;
            this.activeActions.create = false;
        }
        const options = await originalLoadOptionsSource.apply(this, arguments);
        return options;
    }
});
