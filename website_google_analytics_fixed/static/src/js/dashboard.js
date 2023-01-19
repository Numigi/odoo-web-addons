/*
    © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("website_google_analytic_fixed", function(require) {
"use strict";

require("website.backend.dashboard").include({
    load_analytics_api() {
        this._super.apply(this, arguments);

        if(!gapi.analytics){
            gapi.load('analytics');
            gapi.analytics = {q:[],ready:function(cb){this.q.push(cb);}};
            gapi.analytics.ready(() => this.analytics_create_components());
        }
    },
});
});
