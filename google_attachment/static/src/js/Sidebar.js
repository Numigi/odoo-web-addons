// Copyright 2018 Numigi
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

odoo.define("google_attachment.Sidebar", function(require) {
"use strict";

var ajax = require("web.ajax");
var Class = require("web.Class");
var core = require("web.core");
var Sidebar = require("web.Sidebar");

var QWeb = core.qweb;
var _t = core._t;

var GoogleOAuthAuthenticator = require("google_attachment.GoogleOAuthAuthenticator");
var GooglePickerManager = require("google_attachment.GooglePickerManager");


function addImportFromGoogleToSideBar(clientId, apiKey){

    var scope = "https://www.googleapis.com/auth/drive";
    var authenticator = new GoogleOAuthAuthenticator(clientId, scope);
    var googlePickerManager = new GooglePickerManager(authenticator, apiKey);

    Sidebar.include({
        _redraw() {
            var self = this;
            this._super.apply(this, arguments);

            // Open a new page when clicking on an attachment url.
            self.$el.find("a[data-section='files']").attr("target", "_new");

            // Add the `From Google ...` button to the sidebar
            var fromGoogleLabel = _t("From Google...");
            var addFromGoogle = $("<li class=\"o_sidebar_add_from_google\"><span>" + fromGoogleLabel + "</span></li>");
            self.$el.find(".o_sidebar_add_attachment").after(addFromGoogle);

            // When clicking on the `From Google ...` button, open the google picker widget.
            addFromGoogle.on("click", function() {
                self.addDocumentsFromPicker();
            });
        },

        /**
         * Open the google picker widget in order to add an attachment.
         */
        addDocumentsFromPicker() {
            var self = this;

            googlePickerManager.getDocumentsFromPicker().then(function(documents){
                // Create all attachments in Odoo.
                var deferredArray = documents.map(function(doc){
                    return self._createAttachmentFromGoogleDriveDoc(doc);
                });

                // Reload the form view when all attachments are created.
                $.when.apply($, deferredArray).then(function(){
                    self.getParent().reload();
                });
            });
        },

        /**
         * Create an attachment in Odoo given the properties of a google document.
         *
         * @param {Object} doc - the properties of the google document to attach.
         */
        _createAttachmentFromGoogleDriveDoc(doc){
            var attachmentValues = {
                name: doc.name,
                type: "url",
                url: doc.url,
                res_id: this.env.activeIds[0],
                res_model: this.env.model,
            };

            return ajax.rpc("/web/dataset/call_kw/ir.attachment/create", {
                model: "ir.attachment",
                method: "create",
                args: [attachmentValues],
                kwargs: {},
            });
        },
    });
}

ajax.rpc("/web/dataset/call_kw/ir.config_parameter/get_google_attachment_parameters", {
    model: "ir.config_parameter", method: "get_google_attachment_parameters", args: [], kwargs: {},
}).then(function(parameters){
    if(parameters.clientId && parameters.apiKey){
        addImportFromGoogleToSideBar(parameters.clientId, parameters.apiKey);
    }
    else {
        console.error(
            "Could not load the javascript assets for the module google_attachment. " +
            "The system parameters google_attachment.client_id and google_attachment.api_key " +
            "must be set by the system administrator."
        );
    }
});

});
