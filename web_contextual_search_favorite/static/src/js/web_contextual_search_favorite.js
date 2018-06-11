/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_contextual_search_favorite", function(require) {
    "use strict";

var core = require("web.core");
var Context = require("web.Context");
var data_manager = require("web.data_manager");
var pyeval = require("web.pyeval");
var session = require("web.session");

var _t = core._t;


/**
 * Extract the content from a domain filter.
 *
 * The given domain can either be an array or a raw string domain.
 *
 * For example, "[('partner_id', '=', 1), ('number', '=',' '123')]"
 * will return "('partner_id', '=', 1), ('number', '=',' '123')".
 *
 * @param {String | Array} the domain to parse
 * @returns {String} the content of the domain
 */
function extractContentFromDomain(domain){
    if(domain instanceof Array){
        domain = JSON.stringify(domain);
    }
    var regex = /^\s*\[([\S\s]*)?\]\s*$/;
    var match = regex.exec(domain);
    if(match === null){
        throw new Error("Invalid domain filter " + domain);
    }
    return match[1];
}


/**
 * Add explicit & operators to a domain content.
 *
 * In Odoo, & operators are implicit in a domain content when neither & not |
 * is specified. This methods adds explicit & operators where these are implicit.
 *
 * @param {String} the domain content with missing & operators
 * @returns {String} the content of the domain
 */
function addExplicitAndOperatorsToDomainContent(domainContent){
    var and = "\"&\"";
    var or = "\"|\"";
    var not = "\"!\"";

    // Standardize quotes around & and | operators
    domainContent = domainContent.replace("'&'", and).replace("'|'", or).replace("'!'", not);

    var domainNodes = [];
    var currentNode = "";
    var parenthesisCount = 0;

    // Iterate around each caracters
    //
    // When encountering an opening, a closing parenthesis or a comma,
    // we determine whether a domain part begins or ends.
    for(var i = 0; i < domainContent.length; i++){
        var char = domainContent[i];

        if(char === "("){
            if(parenthesisCount === 0){
                domainNodes.push(currentNode);
                currentNode = "";
            }
            currentNode += char;
            parenthesisCount += 1;
        }
        else if(char === ")"){
            parenthesisCount -= 1;
            currentNode += char;
            if(parenthesisCount === 0){
                domainNodes.push(currentNode);
                currentNode = "";
            }
        }
        else if(parenthesisCount === 0 && char === ","){
            domainNodes.push(currentNode);
            currentNode = "";
        }
        else{
            currentNode += char;
        }
    }

    domainNodes.push(currentNode);

    // Exclude empty strings and strings containing only spaces
    domainNodes = domainNodes.map(function(n){return n.trim()}).filter(function(n){return n});

    var operators = domainNodes.filter(function(n){return n === and || n === or});
    var comparisons = domainNodes.filter(function(n){return n !== and && n !== or && n !== not});

    // The total number of & and | operators must be equal to the number of comparisons - 1.
    var missingAnds = _.times(comparisons.length - operators.length - 1, _.constant(and));
    return missingAnds.concat(domainNodes).join(",");
}


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
        var filter_name = this.$inputs[0].value;
        var default_filter = this.$inputs[1].checked;
        var shared_filter = this.$inputs[2].checked;

        if (!filter_name.length){
            this.do_warn(_t("Error"), _t("Filter name is required."));
            this.$inputs.first().focus();
            return;
        }

        if (_.chain(this.filters)
                .pluck("name")
                .contains(filter_name).value()) {
            this.do_warn(_t("Error"), _t("Filter with same name already exists."));
            this.$inputs.first().focus();
            return;
        }

        var user_context = this.getSession().user_context;
        var search = this.searchview.build_search_data();
        var controllerContext;
        this.trigger_up("get_controller_context", {
            callback(ctx) {
                controllerContext = ctx;
            },
        });

        var results = pyeval.eval_domains_and_contexts({
                domains: search.domains,
                contexts: [user_context].concat(search.contexts.concat(controllerContext || [])),
                group_by_seq: search.groupbys || [],
            });

        if (!_.isEmpty(results.group_by)) {
            results.context.group_by = results.group_by;
        }

        var ctx = results.context;
        _(_.keys(session.user_context)).each(function (key) {
            delete ctx[key];
        });

        // Only the following lines were modified in the method
        var domainContents = search.domains.map(extractContentFromDomain)
        var domain = "[" + domainContents.join(",") + "]";
        // Modifed lines end here

        var filter = {
            name: filter_name,
            user_id: shared_filter ? false : session.uid,
            model_id: this.target_model,
            context: results.context,
            domain: domain,
            sort: JSON.stringify(this.searchview.dataset._sort),
            is_default: default_filter,
            action_id: this.action_id,
        };
        return data_manager.create_filter(filter).done(function (id) {
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
        var search_data = this.searchview.build_search_data();

        var context = new Context(this.searchview.dataset.get_context() || []);
        _.each(search_data.contexts, context.add, context);

        // Only the following lines were modified in the method
        var domains = (this.searchview.dataset.get_domain() || []).concat(search_data.domains);
        var domainContents = domains.map(extractContentFromDomain);
        var domain = "[" + domainContents.join(",") + "]";
        // Modifed lines end here

        context.add({
            group_by: pyeval.eval("groupbys", search_data.groupbys || []),
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
                domain: domain,
                view_mode: self.view_manager.active_view.type,
                name: name,
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

require("web.search_inputs").FilterGroup.include({
    /**
     * When clicking on an item in the Filters dropdown, render a contextual domain filter.
     *
     * This method was copied and adapted from the source code of Odoo:
     *
     * odoo/addons/web/static/src/js/chrome/search_inputs.js
     */
    get_domain(facet) {
        var userContext = this.getSession().user_context;
        var domains = facet.values.chain()
            .map(function (f) { return f.get("value").attrs.domain; })
            .without("[]")
            .reject(_.isEmpty)
            .value();

        var domainContents = domains.map(extractContentFromDomain);
        var domainContentsWithExplicitAnds = domainContents.map(addExplicitAndOperatorsToDomainContent);
        var ors = _.times(domainContentsWithExplicitAnds.length - 1, _.constant("\"|\""));
        return "[" + ors.concat(domainContentsWithExplicitAnds).join(",") + "]";
    },
});


var oldEval = pyeval.eval;

/**
 * Patch pyeval to add missing contextual variables if undefined.
 *
 * One very important variable is uid, which is used for filtering
 * records created by the user or for which the user is responsible.
 */
pyeval.eval = function(type, object, context){
    return oldEval(type, object, new Context(session.user_context, context));
};

});
