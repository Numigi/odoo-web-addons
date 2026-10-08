/* Copyright 2026 Numigi Solutions
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('website_sale_carrier_account.checkout', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteSaleCarrierAccount = publicWidget.Widget.extend({
        selector: '#delivery_carrier',
        events: {
            'click .o_delivery_carrier_select': '_onCarrierClick',
            'change .carrier_account_input': '_onCarrierNumberChange',
        },

        start: function () {
            this._toggleCarrierInput();
            return this._super.apply(this, arguments);
        },

        _onCarrierClick: function (ev) {
            var carrierId = $(ev.currentTarget).find('input[name="delivery_type"]').val();
            this._toggleCarrierInput(carrierId);
        },

        _toggleCarrierInput: function (carrierId) {
            this.$('.carrier_account_container').addClass('d-none');

            if (!carrierId) {
                carrierId = this.$('input[name="delivery_type"]:checked').val();
            }

            if (carrierId) {
                this.$('#carrier_account_container_' + carrierId).removeClass('d-none');
            }
        },

        _onCarrierNumberChange: function (ev) {
            var accountNum = $(ev.currentTarget).val();
            ajax.jsonRpc('/shop/carrier_account/update', 'call', {
                'carrier_account_number': accountNum
            });
        },
    });

    return publicWidget.registry.WebsiteSaleCarrierAccount;
});
