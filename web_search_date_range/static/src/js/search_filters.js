/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_search_date_range.filter_menu_with_date_range", function(require) {
    "use strict";

var Class = require("web.Class");
var Widget = require("web.Widget");
var FilterMenu = require("web.FilterMenu");
var searchInputs = require("web.search_inputs");
var pyeval = require("web.pyeval");
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


/**
 * A clickable list item widget used to show / hide the filters of a given field.
 */
var SearchDateRangeProposition = Widget.extend({
    template: "web_search_date_range.search_date_range_proposition",
    init(parent, label){
        this._super.apply(this, arguments);
        this.label = label;
    },
});


FilterMenu.include({
    events: _.extend({}, FilterMenu.prototype.events, {
        "click .o_add_date_range": "append_date_range_proposition",
    }),
    start(){
        this._super.apply(this, arguments);
        var self = this;

        var model = this.searchview.dataset.model;
        filterRegistry.getFilters(model).then(function(filterArray){
            // Group the filters by field
            var filterArraysByField = _.values(_.groupBy(filterArray, function(f){return f.field;}));

            // Sort the filter groups by label
            var sortedFilterArrays = _.sortBy(filterArraysByField, function(filterArray){
                return filterArray[0].field_label;
            });

            // Render each group of filters
            sortedFilterArrays.forEach(function(filterArrayForSingleField){
                self._addFilterWidgetsForSingleField(filterArrayForSingleField);
            });
        });
    },
    /**
     * Add the date filters related to a single field to the search view.
     *
     * @param {Array} filterArray - an array of filters that belong to the same field.
     */
    _addFilterWidgetsForSingleField(filterArray) {
        var sortedfilterArray = filterArray.sort(function(f){return -f.sequence;});

        var self = this;
        var proposition = new SearchDateRangeProposition(this, sortedfilterArray[0].field_label);
        proposition.insertBefore(this.$add_filter);

        // Create the search items
        var filterWidgets = sortedfilterArray.map(function(filter){
            return self._createDateRangeFilterWidget(filter);
        });
        var filterGroup = new searchInputs.FilterGroup(filterWidgets, this.searchview);
        filterGroup.insertBefore(this.$add_filter);
        $("<li class=\"divider\">").insertBefore(this.$add_filter);

        // Show / hide filters when clicking on the field name
        proposition.$el.click(function(){
            proposition.$el.toggleClass("o_closed_menu");
            proposition.$el.toggleClass("o_open_menu");
            filterGroup.$el.toggle();
        });

        // Hide filters by default
        proposition.$el.addClass("o_closed_menu");
        filterGroup.$el.hide();
    },
    /**
     * Create a single filter widget.
     *
     * @param {Object} filter - the filter values
     */
    _createDateRangeFilterWidget(filter) {
        var filterXMLNode = {
            attrs: {
                name: filter.technical_name,
                domain: filter.domain,
                string: filter.label,
            },
            children: [],
            tag: "filter",
        };
        return new searchInputs.Filter(filterXMLNode, this.searchview);
    },
});

});
