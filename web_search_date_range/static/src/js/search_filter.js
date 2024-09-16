/** @odoo-module **/

import { rpc } from 'web.rpc';

export class SearchDateRange {
    constructor(){
        this._deferred = this._createDeferred();
        this._filtersFetched = false;
        this._filtersByModel = new Map();
    }


    _createDeferred(){
        let resolve;
        const promise = new Promise((res) => {
            resolve = res;
        });
        promise.resolve = resolve; 
        return promise;
    }

    /**
     * Get an array of filter values for the given model.
     *
     * @param {String} model: the model name
     * @returns {Promise<Array>} A promise that resolves to an array of filters.
     */
    getFilters(model) {
        if (!this._filtersFetched) {
            this._fetchFilters().then(() => {
                this._deferred.resolve(); // Resolve after fetching filters
            });
            this._filtersFetched = true;
        }

        return this._deferred.then(() => {
            return this._filtersByModel.get(model) || [];
        });
    }

    /**
     * Fetch the filters from the server.
     *
     * All filters are cached on the first query.
     * This method is called only one time per session.
     */
    _fetchFilters() {
        return rpc.query({
            model: "search.date.range.filter",
            method: "get_filter_list",
            args: [],
            kwargs: {},
        }).then((result) => {
            result.forEach((filter) => {
                if (!this._filtersByModel.has(filter.model)) {
                    this._filtersByModel.set(filter.model, []);
                }
                this._filtersByModel.get(filter.model).push(filter);
            });
        });
    }
}
