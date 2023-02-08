odoo.define('web_search_date_range.FilterMenu', function (require) {
    "use strict";

    const CustomFilterItem = require('web.CustomFilterItem');
    const DropdownMenu = require('web.DropdownMenu');
    const { FACET_ICONS } = require("web.searchUtils");
    const { useModel } = require('web/static/src/js/model.js');
        var Class = require("web.Class");
var Widget = require("web.Widget");
//var FilterMenu = require("web.FilterMenu");
//var searchInputs = require("web.search_inputs");
var ajax = require("web.ajax");
const FilterMenu = require('web.FilterMenu');
const ControlPanel = require('web.ControlPanel');
console.log('----------------------------------------ControlPanel');
console.log(ControlPanel.components);


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

var SearchDateRangeProposition = Widget.extend({
    template: "web_search_date_range.search_date_range_proposition",
    init(parent, label){
        this._super.apply(this, arguments);
        this.label = label;
    },
});

class FilterMenuCustom extends FilterMenu{

       constructor() {
            super(...arguments);

            console.log('----------------------------------------gggg');

            this.model = useModel('searchModel');
            this.add_filter();

        }
        add_filter() {
    var self = this;
        filterRegistry.getFilters(this.model.config.modelName).then(function(filterArray){
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
        }
    _addFilterWidgetsForSingleField(filterArray) {
        var sortedfilterArray = filterArray.sort(function(f){return -f.sequence;});

        var self = this;
        var proposition = new SearchDateRangeProposition(this, sortedfilterArray[0].field_label);
        /*var filterWidgets = sortedfilterArray.map(function(filter){
            return self._createDateRangeFilterWidget(filter);
        });*/




 var prefilter = [];
        sortedfilterArray.forEach(function(filter){

        prefilter.push({
            description: filter.label,
            domain: filter.domain,
            name: filter.technical_name,
            type: 'filter',
        });
        });


         this.model.dispatch('createNewFiltersDateRange', prefilter);



        /*var filterGroup = new searchInputs.FilterGroup(filterWidgets, this.getParent(), {}, {});
        filterGroup.insertBefore(this.$addCustomFilter);
        $("<li class=\"divider\">").insertBefore(this.$addCustomFilter);*/

        // Show / hide filters when clicking on the field name

    }

    _createDateRangeFilterWidget(filter) {


    }


    }

    ControlPanel.components["FilterMenu"] = FilterMenuCustom;
    return FilterMenuCustom



});