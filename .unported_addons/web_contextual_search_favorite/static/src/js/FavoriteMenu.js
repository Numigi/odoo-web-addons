/*
    © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_contextual_search_favorite.FavoriteMenu", function(require) {
    "use strict";

var ActionManager = require("web.ActionManager");
var Context = require("web.Context");
var core = require("web.core");
var Domain = require("web.Domain");
var FavoriteMenu = require("web.FavoriteMenu");
var pyUtils = require("web.py_utils");

var _t = core._t;

var mergeDomainsWithAndOperators = webContextualSearchFavorite.domainParsing.mergeDomainsWithAndOperators;


require("web.FavoriteMenu").include({
    /**
     * When adding a filtered view to the dashboard, render a contextual domain filter.
     *
     * This method was copied and adapted from the source code of Odoo:
     *
     * odoo/addons/board/static/src/js/favorite_menu.js
     */
    _addDashboard(){
        var self = this;
        var searchData = this.searchview.build_search_data(true);

        var context = new Context(this.searchview.dataset.get_context() || []);
        _.each(searchData.contexts, context.add, context);

        // Only the following lines were modified in the method
        const searchDomain = this.searchview.dataset.get_domain()
        var domains = (searchDomain ? [searchDomain] : []).concat(searchData.domains);
        var domain = mergeDomainsWithAndOperators(domains);
        // Modifed lines end here

        context.add({
            group_by: pyUtils.eval("groupbys", searchData.groupbys || []),
        });
        // AAB: trigger_up an event that will be intercepted by the controller,
        // as soon as the controller is the parent of the control panel
        var am = this.findAncestor(function (a) {
            return a instanceof ActionManager;
        });
        // with options "keepSearchView", it may happen that the action_id of
        // the searchview (received in init) is not the one of the current
        // action, which corresponds to the one we want to add to dashboard
        var currentAction = am.getCurrentAction();
        var controller = am.getCurrentController();
        context.add(controller.widget.getContext());
        var c = pyUtils.eval("context", context);
        for (var k in c) {
            if (c.hasOwnProperty(k) && /^search_default_/.test(k)) {
                delete c[k];
            }
        }
        this._toggleDashboardMenu(false);
        c.dashboard_merge_domains_contexts = false;
        var name = self.$add_dashboard_input.val();

        return self._rpc({
            route: "/board/add_to_dashboard",
            params: {
                action_id: currentAction.id || false,
                context_to_save: c,
                domain: domain,
                view_mode: controller.viewType,
                name: name,
            },
        })
        .then(function (r) {
            if (r) {
                self.do_notify(
                    _.str.sprintf(_t("'%s' added to dashboard"), name),
                    _t("Please refresh your browser for the changes to take effect.")
                );
            } else {
                self.do_warn(_t("Could not add filter to dashboard"));
            }
        });
    },
});

});
