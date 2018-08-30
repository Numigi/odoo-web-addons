/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_search_date_range_account.pyeval", function(require) {
"use strict";

var pyeval = require("web.pyeval");
var session = require("web.session");

var oldEval = pyeval.eval;

/**
 * Convert the given date string into a python (py.js) datetime object.
 */
function toDatetime(dateString){
    var date = moment(dateString).toDate();
	var datetime = pyeval.context().datetime;
    return py.PY_call(datetime.date, [date.getFullYear(), date.getMonth() + 1, date.getDate()]);
}

var fiscalYearData = {
    fiscal_year_start: toDatetime(session.fiscal_year_start),
    trimester_start: toDatetime(session.trimester_start),
};

/**
 * Add the fiscal year data to the pyeval function.
 */
pyeval.eval = function(type, object, context){
    return oldEval(type, object, _.extend({}, fiscalYearData, context || {}));
};

});
