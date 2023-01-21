odoo.define('web_search_date_range.FilterMenu', function (require) {
    "use strict";

var FilterMenu = require("web.FilterMenu");
var DropdownMenu = require("web.DropdownMenu");
const CustomFilterItem = require('web.CustomFilterItem');
console.log(FilterMenu.props);

class FilterMenuCustom extends FilterMenu {
start(){
this._super.apply(this, arguments);
        console.log("------------------------------test----------------filterRegistry");

            var self = this;

        var model = "res.partner";
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
        }
    }
    FilterMenuCustom.components = Object.assign({},  DropdownMenu.components, {
    CustomFilterItem
    });
    FilterMenuCustom.props = Object.assign({}, DropdownMenu.props, {
        fields: Object,
    });

    return FilterMenuCustom;


});