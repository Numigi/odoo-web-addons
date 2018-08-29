/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_contextual_search_favorite.pyeval", function(require) {
    "use strict";

var Context = require("web.Context");
var pyeval = require("web.pyeval");
var session = require("web.session");

var oldEval = pyeval.eval;

/**
 * Variables required when filtering using `Active` filters (TA#4193).
 */
var extraPythonGlobals = {
    "true": true,
    "false": false,
};

/**
 * Patch pyeval to add missing contextual variables if undefined.
 *
 * One very important variable is uid, which is used for filtering
 * records created by the user or for which the user is responsible.
 */
pyeval.eval = function(type, object, context){
    return oldEval(type, object, _.extend({}, extraPythonGlobals, session.user_context, context || {}));
};

/**
 * Redefine pyeval.eval_domains_and_contexts to point on the extended version of pyeval.eval.
 */
pyeval.eval_domains_and_contexts = function(source){
    return {
        context: pyeval.eval("contexts", source.contexts || [], source.eval_context),
        domain: pyeval.eval("domains", source.domains, source.eval_context),
        group_by: pyeval.eval("groupbys", source.group_by_seq || [], source.eval_context),
    };
};

});
