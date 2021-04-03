/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_search_date_range/static/src/js/search_filters.js", function(require) {
    "use strict";

var Class = require("web.Class");
var ajax = require("web.ajax");


/**
 * A class responsible for managing the metadata related to date filters.
 */
var DateRangeFilterRegistry = Class.extend({
    init(){
        this._deferred = new $.Deferred();
        this._filtersFetched = false;
        this._filtersByModel = new Map();
    },
    /**
     * Get an array of filter values for the given model.
     *
     * @param {String} model: the model name
     */
    getFilters(model){
        var self = this;

        if(!this._filtersFetched){
            this._fetchFilters().then(function(){
                self._deferred.resolve();
            });
            this._filtersFetched = true;
        }

        return $.when(this._deferred).then(function(){
            return self._filtersByModel.get(model) || [];
        });
    },
    /**
     * Fetch the filters from the server.
     *
     * All filters are cached on the first query.
     * This method is called only one time per session.
     */
    _fetchFilters(){
        var self = this;
        return ajax.rpc("/web/dataset/call_kw/search.date.range.filter/get_filter_list", {
            model: "search.date.range.filter",
            method: "get_filter_list",
            args: [],
            kwargs: {},
        }).then(function(result){
            result.forEach(function(filter){
                if(!self._filtersByModel.has(filter.model)){
                    self._filtersByModel.set(filter.model, []);
                }
                self._filtersByModel.get(filter.model).push(filter);
            });
        });
    },
});

var filterRegistry = new DateRangeFilterRegistry();

return filterRegistry

});
