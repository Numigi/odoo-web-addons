// Copyright 2023 Numigi
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
        this._scope = scope
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
        const self = this;
        const deferred = new $.Deferred();

        this._loadApi().then(function(){
            self._googleAuth = gapi.auth2.init({client_id: self._clientId});
            self._googleAuth.then(function(){
                if(self._isSignedIn()){
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

    getToken(){
        const user = this._getOauthUser()
        const data = user.getAuthResponse(true)
        return data.access_token;
    },

    _isSignedIn() {
        if (!this._googleAuth.isSignedIn.get()) {
            return false
        }
        const user = this._getOauthUser()
        return user.hasGrantedScopes(this._scope)
    },

    _loadApi(){
        const deferred = new $.Deferred();

        if(this._apiLoaded){
            deferred.resolve();
        }
        else {
            const self = this;
            gapi.load("auth2", function(){
                self._apiLoaded = true;
                deferred.resolve();
            });
        }

        return deferred;
    },

    _getOauthUser() {
        return this._googleAuth.currentUser.get();
    },
});

return GoogleOAuthAuthenticator;

});
