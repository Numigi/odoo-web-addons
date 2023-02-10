odoo.define('web_contextual_search_favorite.AddToBoardMenu', function (require) {
    "use strict";
    const Context = require('web.Context');
    const Domain = require('web.Domain');
    const FavoriteMenu = require('web.FavoriteMenu');
    const { sprintf } = require('web.utils');
    const { useAutofocus } = require('web.custom_hooks');

    var mergeDomainsWithAndOperators = webContextualSearchFavorite.domainParsing.mergeDomainsWithAndOperators;
    const AddToBoardMenu = FavoriteMenu.registry.get('add-to-board-menu');

class AddToBoardMenuCustom extends AddToBoardMenu {
     /**
     * When adding a filtered view to the dashboard, render a contextual domain filter.
     *
     * This method was copied and adapted from the source code of Odoo:
     *
     * odoo/addons/board/static/src/js/add_to_board_menu.js
     */

     async _addToBoard() {
        const searchModel = this.env.searchModel;
        const searchQuery = searchModel.get('query');
        const context = new Context(this.env.action.context);
        context.add(searchQuery.context);

        context.add({
            group_by: searchQuery.groupBy,
            orderedBy: searchQuery.orderedBy,
        });

        if (searchQuery.timeRanges && searchQuery.timeRanges.hasOwnProperty('fieldName')) {
            context.add({
                comparison: searchQuery.timeRanges,
            });
        }
        let controllerQueryParams;
        this.env.searchModel.trigger('get-controller-query-params', params => {
            controllerQueryParams = params || {};
        });
        controllerQueryParams.context = controllerQueryParams.context || {};
        const queryContext = controllerQueryParams.context;
        delete controllerQueryParams.context;
        context.add(Object.assign(controllerQueryParams, queryContext));

        // Only the following lines were modified in the method
        const domain1 = this.env.action.domain || [];

        const controlPanelModelExtension  = searchModel.extensions[0].find(
        (ext) => ext.constructor.name === "ControlPanelModelExtension" || ext.constructor.name === "ControlPanelModelExtensionCustom" ||
        ext.constructor.name === "ControlPanelExtension");
        const groups = controlPanelModelExtension._getGroups();
        var domain2 = [controlPanelModelExtension._getDomain(groups)];
        var domains = (domain1 ? [domain1] : []).concat(domain2)
        var domain = mergeDomainsWithAndOperators(domains);
        // Modifed lines end here

        const evalutatedContext = context.eval();
        for (const key in evalutatedContext) {
            if (evalutatedContext.hasOwnProperty(key) && /^search_default_/.test(key)) {
                delete evalutatedContext[key];
            }
        }
        evalutatedContext.dashboard_merge_domains_contexts = false;

        Object.assign(this.state, {
            name: $(".o_input").val() || "",
            open: false,
        });

        const result = await this.rpc({
            route: '/board/add_to_dashboard',
            params: {
                action_id: this.env.action.id || false,
                context_to_save: evalutatedContext,
                domain: domain,
                view_mode: this.env.view.type,
                name: this.state.name,
            },
        });
        if (result) {
            this.env.services.notification.notify({
                title: sprintf(this.env._t("'%s' added to dashboard"), this.state.name),
                message: this.env._t("Please refresh your browser for the changes to take effect."),
                type: 'warning',
            });
        } else {
            this.env.services.notification.notify({
                message: this.env._t("Could not add filter to dashboard"),
                type: 'danger',
            });
        }
    }
    }

FavoriteMenu.registry.add('add-to-board-menu', AddToBoardMenuCustom, 10);

return AddToBoardMenuCustom;

});
