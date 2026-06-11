/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { session } from "@web/session";

export class DbNameSystrayItem extends Component {
    setup() {
        // Fetch the database name from the user session
        this.dbName = session.db;
    }
}

// Bind the component to its XML template
DbNameSystrayItem.template = "web_db_name_display.DbNameSystrayItem";

// Add the component to the top bar (systray)
// The sequence defines its position relative to other icons (e.g., 15 usually places it to the left of the debug/profile menu)
registry.category("systray").add("web_db_name_display.DbNameSystrayItem", {
    Component: DbNameSystrayItem,
}, { sequence: 15 });