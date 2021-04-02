odoo.define("web_search_date_range/static/src/js/control_panel_model_extension.js", function (require) {
    "use strict";

require("web/static/src/js/control_panel/control_panel_model_extension.js");

const ActionModel = require("web/static/src/js/views/action_model.js");
const ControlPanel = ActionModel.registry.get("ControlPanel")
const pyUtils = require('web.py_utils')
const filterRegistry = require("web_search_date_range/static/src/js/search_filters.js")


class ControlPanelExtension extends ControlPanel {

    constructor() {
        super(...arguments);
        this.relativeDateOptions = []

        filterRegistry.getFilters(this.config.modelName).then((filters) => {
            this.relativeDateOptions = filters
        })
    }

    _addFilters() {
        super._addFilters()

        const pregroup = [
            {
                description: "My Filter",
                type: "filter",
                isDefault: false,
                isRelativeDateFilter: true,
            }
        ]

        this._createGroupOfFilters(pregroup);
    }

    _enrichFilterCopy(filter, filterQueryElements) {
        if (!filter.isRelativeDateFilter) {
            return super._enrichFilterCopy(filter, filterQueryElements)
        }

        const isActive = Boolean(filterQueryElements.length);
        const f = Object.assign({ isActive }, filter);

        function _enrichOptions(options) {
            return options.map(o => {
                const { description, id, groupNumber } = o;
                const isActive = filterQueryElements.some(a => a.optionId === id);
                return { description, id, groupNumber, isActive };
            });
        }

        f.options = _enrichOptions(this.relativeDateOptions);

        return f;
    }

    toggleFilterWithOptions(filterId, optionId) {
        const filter = this.state.filters[filterId];
        if (!filter.isRelativeDateFilter) {
            return super.toggleFilterWithOptions(filterId, optionId)
        }

        const index = this.state.query.findIndex(
            queryElem => queryElem.filterId === filterId && queryElem.optionId === optionId
        );

        if (index >= 0) {
            this.state.query.splice(index, 1);
        } else {
            this.state.query.push({ groupId: filter.groupId, filterId, optionId });
        }
    }

    _getFilterDomain(filter, filterQueryElements) {
        if (!filter.isRelativeDateFilter) {
            return super._getFilterDomain(filter, filterQueryElements);
        }

        const { fieldName, fieldType } = filter;
        const options = this._getSelectedRelativeDateOptions(filterQueryElements)
        const domains = options.map(o => JSON.stringify(o.domain))
        return pyUtils.assembleDomains(domains, 'OR')
    }

    _getFacetDescriptions(activities, type) {
        if (type === "field" || type === "groupBy") {
            return super._getFacetDescriptions(activities, type)
        }

        const descriptions = [];
        let description;

        for (const activity of activities) {
            if (activity.filter.isRelativeDateFilter) {
                description = this._getRelativeDateFilterDescription(activity)
            }
            else {
                description = super._getFacetDescriptions([activity], type)[0]
            }
            descriptions.push(description);
        }
        return descriptions
    }

    _getRelativeDateFilterDescription(activity) {
        const { filter, filterQueryElements } = activity
        const options = this._getSelectedRelativeDateOptions(filterQueryElements)
        return filter.description + ': ' + options.map(o => o.description).join(" | ")
    }

    _getSelectedRelativeDateOptions(filterQueryElements) {
        const optionIds = filterQueryElements.map(el => el.optionId);
        return this.relativeDateOptions.filter(o => optionIds.indexOf(o.id) !== -1)
    }
}

ActionModel.registry.add("ControlPanel", ControlPanelExtension, 10);

});
