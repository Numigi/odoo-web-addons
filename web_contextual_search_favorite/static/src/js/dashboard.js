odoo.define("web_contextual_search_favorite.dashboard", function (require) {
"use strict";

require("board.dashboard");
var FormRenderer = require("web.FormRenderer");

FormRenderer.include({
    /**
     * Stringify the domain when generating the architecture or the board.
     *
     * Without this method, the domain is passed as a javascript object to QWeb
     * and is not rendered properly.
     *
     * In the source code of Odoo, the same logic is applied to modifiers.
     * See method getBoard in odoo/addons/board/static/src/js/board_view.js.
     */
    getBoard() {
        var result = this._super.apply(this, arguments);
        result.columns.forEach((column) => {
            column.forEach((action) => {
                if(action.domain){
                    action.domain = JSON.stringify(action.domain);
                }
            });
        });
        return result;
    },
});

});
