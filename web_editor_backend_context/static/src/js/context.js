/*
    © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("web_editor_backend_context.context", function(require) {
"use strict";

const functions = require("web_editor.context")

const oldGetContext = functions.get
const oldGetExtraContext = functions.getExtra

function addUserContext(context) {
    return _.extend(odoo.session_info.user_context, context)
}

function getContext(context) {
    context = addUserContext(context)
    return oldGetContext(context)
}

function getExtraContext(context) {
    context = addUserContext(context)
    return oldGetExtraContext(context)
}

functions.get = getContext
functions.getExtra = getExtraContext

});
