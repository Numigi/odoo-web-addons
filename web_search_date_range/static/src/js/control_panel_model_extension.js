odoo.define("web_search_date_range/static/src/js/search.js", function (require) {
    "use strict";

    var ControlPanelModelExtension = require("web/static/src/js/control_panel/control_panel_model_extension.js");
    const ActionModel = require("web/static/src/js/views/action_model.js");
    let filterId = 1;
    let groupId = 1;
    let groupNumber = 1;


class ControlPanelModelExtensionCustom  extends ControlPanelModelExtension{
     constructor() {
            super(...arguments);
           }
           createNewFiltersDateRange(prefilters) {
            if (!prefilters.length) {
                return [];
            }
            const newFilterIdS = [];
            prefilters.forEach(preFilter => {
                const filter = Object.assign(preFilter, {
                    groupId,
                    groupNumber,
                    id: filterId,
                    type: 'filter',
                });
                this.state.filters[filterId] = filter;
                //this.state.query.push({ groupId, filterId });
                newFilterIdS.push(filterId);
                filterId++;
            });
            groupId++;
            groupNumber++;
            return newFilterIdS;
        }

     }



    ActionModel.registry.add("ControlPanel", ControlPanelModelExtensionCustom, 10);

    return ControlPanelModelExtensionCustom;
    });