/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SearchModel } from "@web/search/search_model";
import { SearchDateRange } from "./search_filter";
import pyUtils from "web.py_utils";

const searchDateRange = new SearchDateRange();

patch(SearchModel.prototype, "web_search_date_range.SearchModel", {
    _enrichItem(searchItem) {
        const item = this._super(...arguments);
        if (item.isRelativeDateFilter !== true) {
            return item;
        }

        const queryElements = this.query.filter(
            (queryElem) => queryElem.searchItemId === searchItem.id
        );
        const isActive = Boolean(queryElements.length);
        const enrichSearchItem = { ...searchItem, isActive };

        const _enrichOptions = (options = [], selectedIds = []) =>
            options.map(({ description, id, groupNumber }) => ({
                description,
                id,
                groupNumber,
                isActive: selectedIds.includes(id),
            }));

        enrichSearchItem.options = _enrichOptions(
            this.custom_options || [],
            queryElements.map((queryElem) => queryElem.generatorId)
        );

        enrichSearchItem.options = _enrichOptions(
            item.custom_options || [],
            queryElements.map((queryElem) => queryElem.generatorId)
        );

        return enrichSearchItem;
    },

    async load() {
        await this._super(...arguments);
        const filteredItems = await searchDateRange.fetchFilters(this.resModel);

        if (filteredItems.length) {
            const searchItemsArray = Array.isArray(this.searchItems) ? this.searchItems : Object.values(this.searchItems);

            filteredItems.forEach(item => {
                if (item.isRelativeDateFilter) {
                    const exists = searchItemsArray.some(searchItem =>
                        searchItem.description === item.description && searchItem.type === item.type
                    );

                    if (!exists) {
                        this._createGroupOfSearchItems([item]);
                    }
                }
            });
        }
    },

    toggleDateFilter(searchItemId, generatorId) {
        const searchItem = this.searchItems[searchItemId];
        if (searchItem.type !== "dateFilter" || searchItem.isRelativeDateFilter !== true) {
            return this._super(...arguments);
        }

        const index = this.query.findIndex(
            (queryElem) =>
                queryElem.searchItemId === searchItemId &&
                queryElem.generatorId === generatorId
        );

        if (index >= 0) {
            this.query.splice(index, 1);
        } else {
            this.query.push({ searchItemId, generatorId });
        }
        this._checkComparisonStatus();
        this._notify();
    },

    _getDateFilterDomain(dateFilter, generatorIds, key = "domain") {
        if (dateFilter.isRelativeDateFilter !== true) {
            return this._super(...arguments);
        }
        const options = this._getSelectedDateRangeOptions(dateFilter, generatorIds);
        const domains = options.map(o => o.domain);

        if (key === "domain") {
            return pyUtils.assembleDomains(domains, 'OR');
        } else if (key === "description") {
            return options.map(o => o.description).join(" | ");
        }
    },

    _getSelectedDateRangeOptions(dateFilter, generatorIds) {
        const optionIds = new Set(generatorIds);
        return dateFilter.custom_options.filter(option => optionIds.has(option.id));
    }
});
