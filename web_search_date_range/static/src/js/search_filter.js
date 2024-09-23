/** @odoo-module **/

import rpc from 'web.rpc';

export class SearchDateRange {
    constructor() {
        this._filtersByModel = new Map();
    }

    async fetchFilters(model) {
        const result = await rpc.query({
            model: "search.date.range.filter",
            method: "get_filter_list",
            args: [],
            kwargs: {},
        });
        const filteredResults = result.filter(filter => filter.model === model);

        if (!this._filtersByModel.has(model)) {
            this._filtersByModel.set(model, []);
        }

        this._filtersByModel.get(model).push(...filteredResults);
        
        return filteredResults;
    }
}
