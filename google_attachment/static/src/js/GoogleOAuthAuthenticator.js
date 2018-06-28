// Copyright 2018 Numigi
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

odoo.define("google_attachment.GoogleOAuthAuthenticator", function(require) {
"use strict";

var Class = require("web.Class");

var GoogleOAuthAuthenticator = Class.extend({

    /**
     * @param {String} clientId - the api client id
     * @param {Array[String]} scope - the google api scope
     */
    init(clientId, scope) {
        this._clientId = clientId;
        this._googleAuth = null;
        this._apiLoaded = false;
        this._signInOptions = {
            scope,
            prompt: "select_account",
        };
    },

    /**
     * Authenticate to Google using the oauth2 api.
     *
     * @returns {$.Deferred} a deferred that resolves when the user is authentified.
     */
    authenticate() {
        var self = this;
        var deferred = new $.Deferred();

        this._loadApi().then(function(){
            self._googleAuth = gapi.auth2.init({client_id: self._clientId});
            self._googleAuth.then(function(){
                if(self._googleAuth.isSignedIn.get()){
                    deferred.resolve();
                }
                else{
                    self._googleAuth.signIn(self._signInOptions).then(function(){
                        deferred.resolve();
                    });
                }
            });

        });

        return deferred;
    },


    /**
     * Load the google oauth2 api.
     *
     * @returns {$.Deferred} a deferred that resolves when the api is loaded.
     */
    _loadApi(){
        var deferred = new $.Deferred();

        if(this._apiLoaded){
            deferred.resolve();
        }
        else {
            var self = this;
            gapi.load("auth2", function(){
                self._apiLoaded = true;
                deferred.resolve();
            });
        }

        return deferred;
    },

    /**
     * Get the user's oauth token.
     *
     * @returns {String} the token
     */
    getToken(){
        var user = this._googleAuth.currentUser.get();
        return user.getAuthResponse(true).access_token;
    },
});

return GoogleOAuthAuthenticator;

});
