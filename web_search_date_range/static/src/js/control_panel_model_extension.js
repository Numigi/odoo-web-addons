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
const { useModel } = require('web/static/src/js/model.js');
    let filterId = 1;
    let groupId = 1;
    let groupNumber = 0;

     class ControlPanelModelExtensionCustom  extends ControlPanelModelExtension{
     constructor() {
            super(...arguments);
            //this.houda_model =  useModel('searchModel');

           }
             _createDateRangeFilterWidget(filter) {


    }




        _addFilterWidgetsForSingleField(filterArray) {
        var sortedfilterArray = filterArray.sort(function(f){return -f.sequence;});
var lst = [];
        // Create the search items
for (let i=0;i< sortedfilterArray.length; i++)
{
lst.push({
           tag: "filter",
            attrs: {
                name: sortedfilterArray[i].technical_name,
                domain: sortedfilterArray[i].domain,
                string: sortedfilterArray[i].label,
            },
            children: [],

            });

}

return lst;





    }
async  _getSearchDateRange(){
    var self = this;
    var f = new DateRangeFilterRegistry().getFilters(this.config.modelName);
    var filterArray = await f;
    var filterArraysByField = _.values(_.groupBy(filterArray, function(f){return f.field;}));
    // Sort the filter groups by label
    var sortedFilterArrays = _.sortBy(filterArraysByField, function(filterArray){
        return filterArray[0].field_label;
    });
    // Render each group of filters
    var lst;
    sortedFilterArrays.forEach(function(filterArrayForSingleField){
        lst = self._addFilterWidgetsForSingleField(filterArrayForSingleField);
    });
    return lst;
}

async  useSearchDateRange() {
    var lst = await this._getSearchDateRange();


for (let j=0; j<lst.length;j++)
{
    this.config.archNodes.push(lst[j]);
}

    //prefilter.push(lst);

    // Do something with the lst variable
}



         _createGroupOfFiltersFromArch() {
//var self = this;



this.useSearchDateRange();

       var n = this.config.archNodes;
       console.log('----------------===========------------------------');
       console.log(n);// Create a new filter object
var newFilter = {
    tag: "filter",
    attrs: {
        name: "my_filter",
        domain: "[('customer_rank', '=', 1)]",
        string: "My Filter"
    },
    children: []
};

// Add the new filter to the view's arch object
var view = this.getParent();
view.arch.children.push(newFilter);

// Reload the view
view.reload();



            const preFilters = n.reduce(
                (preFilters, child) => {
                    if (child.tag === 'group') {

                        return [...preFilters, ...child.children.map(c => this._evalArchChild(c))];
                    }
                    else if (child.tag === 'filter') {
                            return [...preFilters, child];
                        }
                    else {

                        return [...preFilters, this._evalArchChild(child)];
                    }
                },
                []
            );
            preFilters.push({ tag: 'separator' });

            console.log('------------------------');
            console.log(preFilters);

            // create groups and filters
            let currentTag;
            let currentGroup = [];
            let pregroupOfGroupBys = [];

            preFilters.forEach(preFilter => {
                if (
                    preFilter.tag !== currentTag ||
                    ['separator', 'field'].includes(preFilter.tag)
                ) {
                    if (currentGroup.length) {
                        if (currentTag === 'groupBy') {
                            pregroupOfGroupBys = [...pregroupOfGroupBys, ...currentGroup];
                        } else {
                            this._createGroupOfFilters(currentGroup);
                        }
                    }
                    currentTag = preFilter.tag;
                    currentGroup = [];
                    groupNumber++;
                }
                if (preFilter.tag !== 'separator') {
                    const filter = {
                        type: preFilter.tag,
                        // we need to codify here what we want to keep from attrs
                        // and how, for now I put everything.
                        // In some sence, some filter are active (totally determined, given)
                        // and others are passive (require input(s) to become determined)
                        // What is the right place to process the attrs?
                    };
                    if (preFilter.attrs && JSON.parse(preFilter.attrs.modifiers || '{}').invisible) {
                        filter.invisible = true;
                        let preFilterFieldName = null;
                        if (preFilter.tag === 'filter' && preFilter.attrs.date) {
                            preFilterFieldName = preFilter.attrs.date;
                        } else if (preFilter.tag === 'groupBy') {
                            preFilterFieldName = preFilter.attrs.fieldName;
                        }
                        if (preFilterFieldName && !this.fields[preFilterFieldName]) {
                            // In some case when a field is limited to specific groups
                            // on the model, we need to ensure to discard related filter
                            // as it may still be present in the view (in 'invisible' state)
                            return;
                        }
                    }
                    if (filter.type === 'filter' || filter.type === 'groupBy') {
                        filter.groupNumber = groupNumber;
                    }
                    this._extractAttributes(filter, preFilter.attrs);
                    currentGroup.push(filter);
                }
            });

            if (pregroupOfGroupBys.length) {
                this._createGroupOfFilters(pregroupOfGroupBys);
            }
            const dateFilters = Object.values(this.state.filters).filter(
                (filter) => filter.isDateFilter
            );
            if (dateFilters.length) {
                this._createGroupOfComparisons(dateFilters);
            }
        }
        _evalArchChild(child) {
            if (child.attrs.context) {
                try {
                    const context = pyUtils.eval('context', child.attrs.context);
                    child.attrs.context = context;
                    if (context.group_by) {
                        // let us extract basic data since we just evaluated context
                        // and use a correct tag!
                        child.attrs.fieldName = context.group_by.split(':')[0];
                        child.attrs.defaultInterval = context.group_by.split(':')[1];
                        child.tag = 'groupBy';
                    }
                } catch (e) { }
            }
            if (child.attrs.name in this.searchDefaults) {
                child.attrs.isDefault = true;
                let value = this.searchDefaults[child.attrs.name];
                if (child.tag === 'field') {
                    child.attrs.defaultValue = this.fields[child.attrs.name].type === 'many2one' && Array.isArray(value) ? value[0] : value;
                } else if (child.tag === 'groupBy') {
                    child.attrs.defaultRank = typeof value === 'number' ? value : 100;
                }



            }
            else if (child.tag == 'filter')
                {
                    return child;
                }
            return child;
        }
        static extractArchInfo(archs) {
            const { attrs, children } = archs.search;
            const controlPanelInfo = {
                attrs,
                children: [],
            };
            for (const child of children) {
                if (child.tag !== "searchpanel") {
                    controlPanelInfo.children.push(child);
                }
            }
            return controlPanelInfo;
        }





      }




    ActionModel.registry.add("ControlPanel", ControlPanelModelExtensionCustom, 10);

    return ControlPanelModelExtensionCustom;
});
