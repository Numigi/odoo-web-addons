odoo.define("web_search_date_range/static/src/js/control_panel_model_extension.js", function (require) {
    "use strict";

    var ControlPanelModelExtension = require("web/static/src/js/control_panel/control_panel_model_extension.js");
    const ActionModel = require("web/static/src/js/views/action_model.js");
    const Domain = require('web.Domain');
    const pyUtils = require('web.py_utils');
    var Class = require("web.Class");
var Widget = require("web.Widget");

//var FilterMenu = require("web.FilterMenu");
//var searchInputs = require("web.search_inputs");
var ajax = require("web.ajax");



    const FAVORITE_PRIVATE_GROUP = 1;
    const FAVORITE_SHARED_GROUP = 2;
    const DISABLE_FAVORITE = "search_disable_custom_filters";
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
var SearchDateRangeProposition = Widget.extend({
    template: "web_search_date_range.search_date_range_proposition",
    init(parent, label){
        this._super.apply(this, arguments);
        this.label = label;
    },
});

var filterRegistry = new DateRangeFilterRegistry();
    let filterId = 1;
    let groupId = 1;
    let groupNumber = 0;

     class ControlPanelModelExtensionCustom  extends ControlPanelModelExtension{
     constructor() {
            super(...arguments);
            console.log("------------------test--------------------------");
           }

      prepareState() {
            Object.assign(this.state, {
                filters: {},
                query: [],
            });
            filterRegistry.getFilters(this.config.).then(function(filterArray){
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


        console.log('-----------------------------------------------------------------');

            if (this.config.withSearchBar !== false) {
                this._addFilters();
                this._activateDefaultFilters();
            }
        }
        _addFilterWidgetsForSingleField(filterArray) {
        var sortedfilterArray = filterArray.sort(function(f){return -f.sequence;});

        var self = this;
//        var proposition = new SearchDateRangeProposition(this, sortedfilterArray[0].field_label);
//        proposition.insertBefore(this.$addCustomFilter);

        // Create the search items
        var filterWidgets = sortedfilterArray.map(function(filter){
            return self._createDateRangeFilterWidget(filter);
        });
        var filterGroup = new searchInputs.FilterGroup(filterWidgets, this.getParent(), {}, {});
        filterGroup.insertBefore(this.$addCustomFilter);
        $("<li class=\"divider\">").insertBefore(this.$addCustomFilter);

        // Show / hide filters when clicking on the field name
        proposition.$el.click(function(){
            var menu = proposition.$el;
            menu.toggleClass("o_closed_menu");
            menu.toggleClass("o_open_menu");

            var subMenu = filterGroup.$el;
            if(subMenu.is(":visible")){
                subMenu.hide();
            }
            else {
                subMenu.show();
            }
        });

        // Hide filters by default
        proposition.$el.addClass("o_closed_menu");
        filterGroup.$el.hide();
    },
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
        return createNewFilters(filterXMLNode)
            //this.model.dispatch('createNewFilters', preFilters);

    },

      }




    ActionModel.registry.add("ControlPanel", ControlPanelModelExtensionCustom, 10);

    return ControlPanelModelExtensionCustom;
});
