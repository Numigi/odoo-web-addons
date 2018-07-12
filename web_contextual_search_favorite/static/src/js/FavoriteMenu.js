/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_contextual_search_favorite.FavoriteMenu", function(require) {
    "use strict";

var Context = require("web.Context");
var core = require("web.core");
var dataManager = require("web.data_manager");
var pyeval = require("web.pyeval");
var session = require("web.session");

var _t = core._t;

var mergeDomainsWithAndOperators = webContextualSearchFavorite.domainParsing.mergeDomainsWithAndOperators;


require("web.FavoriteMenu").include({
    /**
     * When saving a favorite, render a contextual domain filter.
     *
     * This method was copied and adapted from the source code of Odoo:
     *
     * odoo/addons/web/static/src/js/chrome/search_menus.js
     */
    save_favorite(){
        var self = this;
        var filterName = this.$inputs[0].value;
        var defaultFilter = this.$inputs[1].checked;
        var sharedFilter = this.$inputs[2].checked;

        if (!filterName.length){
            this.do_warn(_t("Error"), _t("Filter name is required."));
            this.$inputs.first().focus();
            return;
        }

        if (_.chain(this.filters)
                .pluck("name")
                .contains(filterName).value()) {
            this.do_warn(_t("Error"), _t("Filter with same name already exists."));
            this.$inputs.first().focus();
            return;
        }

        var userContext = this.getSession().user_context;
        var search = this.searchview.build_search_data();
        var controllerContext;
        this.trigger_up("get_controller_context", {
            callback(ctx) {
                controllerContext = ctx;
            },
        });

        // Only the following lines were modified in the method
        var contexts = [userContext].concat(search.contexts).concat(controllerContext || []);
        var filterContext = pyeval.eval("contexts", contexts);

        if (!_.isEmpty(search.groupbys)) {
            filterContext.group_by = pyeval.eval("groupbys", search.groupbys);
        }

        _(_.keys(session.user_context)).each(function (key) {
            delete filterContext[key];
        });

        var domain = mergeDomainsWithAndOperators(search.domains);
        // Modifed lines end here

        var filter = {
            name: filterName,
            user_id: sharedFilter ? false : session.uid,
            model_id: this.target_model,
            context: filterContext,
            domain,
            sort: JSON.stringify(this.searchview.dataset._sort),
            is_default: defaultFilter,
            action_id: this.action_id,
        };
        return dataManager.create_filter(filter).done(function (id) {
            filter.id = id;
            self.toggle_save_menu(false);
            self.$save_name.find("input").val("").prop("checked", false);
            self.add_filter(filter);
            self.append_filter(filter);
            self.toggle_filter(filter, true);
        });
    },
    /**
     * When adding a filtered view to the dashboard, render a contextual domain filter.
     *
     * This method was copied and adapted from the source code of Odoo:
     *
     * odoo/addons/board/static/src/js/favorite_menu.js
     */
    _addDashboard(){
        var self = this;
        var searchData = this.searchview.build_search_data();

        var context = new Context(this.searchview.dataset.get_context() || []);
        _.each(searchData.contexts, context.add, context);

        // Only the following lines were modified in the method
        var domains = (this.searchview.dataset.get_domain() || []).concat(searchData.domains);
        var domain = mergeDomainsWithAndOperators(domains);
        // Modifed lines end here

        context.add({
            group_by: pyeval.eval("groupbys", searchData.groupbys || []),
        });
        context.add(this.view_manager.active_view.controller.getContext());

        var c = pyeval.eval("context", context);
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
                action_id: self.action_id || false,
                context_to_save: c,
                domain,
                view_mode: self.view_manager.active_view.type,
                name,
            },
        })
        .then(function (r) {
            if (r) {
                self.do_notify(_.str.sprintf(_t("'%s' added to dashboard"), name), "");
            } else {
                self.do_warn(_t("Could not add filter to dashboard"));
            }
        });
    },
});

});
