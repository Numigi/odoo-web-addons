// Copyright 2018 Numigi
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

odoo.define("google_attachment.GooglePickerManager", function(require) {
"use strict";

var Class = require("web.Class");

var GooglePickerManager = Class.extend({

    /**
     * @param authenticator {GoogleOAuthAuthenticator}
     * @param developerKey {String} the google drive api key
     */
    init(authenticator, developerKey){
        this._authenticator = authenticator;
        this._developerKey = developerKey;
        this._loaded = false;
    },

    /**
     * Open the google picker widget.
     *
     * An array of selected document properties is returned through the deferred.
     *
     * @returns {$.Deferred} a deferred that resolves when documents are selected.
     */
    getDocumentsFromPicker() {
        var self = this;
        var deferred = new $.Deferred();

        $.when(this._loadApi(), this._authenticator.authenticate()).then(function() {
            var oauthToken = self._authenticator.getToken();
            var userLang = odoo.session_info.user_context.lang || "en_US";
            var origin = window.location.protocol + "//" + window.location.host;

            var view = (
                new google.picker.DocsView(google.picker.ViewId.DOCS)
                .setSelectFolderEnabled(true)
                .setIncludeFolders(true)
            );

            new google.picker.PickerBuilder()
                .addView(view)
                .addView(google.picker.ViewId.RECENTLY_PICKED)
                .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
                .enableFeature(google.picker.Feature.SUPPORT_TEAM_DRIVES)
                .setOAuthToken(oauthToken)
                .setDeveloperKey(self._developerKey)
                .setLocale(userLang)
                .setOrigin(origin)
                .setCallback(function(data){
                    var documents = self._getDocumentPropertiesFromPickerResponse(data);
                    if(documents !== null){
                        deferred.resolve(documents);
                    }
                })
                .build()
                .setVisible(true);
        });

        return deferred;
    },

    /**
     * Load the google picker api.
     *
     * @returns {$.Deferred} a deferred that resolves when the api is loaded.
     */
    _loadApi(){
        var deferred = new $.Deferred();
        if(this._loaded){
            deferred.resolve();
        }
        else {
            var self = this;
            gapi.load("picker", function() {
                deferred.resolve();
                self._loaded = true;
            });
        }
        return deferred;
    },

    /**
     * Get an array of document properties from the response of the picker.
     *
     * If the user did not select documents, return null.
     *
     * @returns {Array | null} the document properties
     */
    _getDocumentPropertiesFromPickerResponse(data){
        if(data[google.picker.Response.ACTION] === google.picker.Action.PICKED) {
            var docs = data[google.picker.Response.DOCUMENTS];
            return docs.map(function(doc){
                return {
                    name: doc[google.picker.Document.NAME],
                    url: doc[google.picker.Document.URL],
                };
            });
        }
        else {
            return null;
        }
    },
});

return GooglePickerManager;

});
