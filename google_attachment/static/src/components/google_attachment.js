// Copyright 2018 Numigi
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

odoo.define("google_attachment/static/src/components/google_attachment.js", function(require) {
"use strict";

const ajax = require("web.ajax");

const GoogleOAuthAuthenticator = require("google_attachment.GoogleOAuthAuthenticator");
const GooglePickerManager = require("google_attachment.GooglePickerManager");

const { Component } = owl;

class GoogleAttachment extends Component {

    async addDocumentsFromPicker() {
        const pickerManager = await getGooglePickerManager()
        pickerManager.getDocumentsFromPicker().then((documents) => {
            const deferredArray = documents.map((doc) => {
                return this._createAttachmentFromGoogleDriveDoc(doc);
            });

            // Reload the form view when all attachments are created.
            $.when.apply($, deferredArray).then(() => {
                this.trigger('o-attachments-changed');
            });
        })
    }
    _createAttachmentFromGoogleDriveDoc(doc){
        var attachmentValues = {
            name: doc.name,
            mimetype: doc.mimetype,
            type: "url",
            url: doc.url,
            res_id: this.props.uploadModel,
            res_model: this.props.uploadId,
        };

        return ajax.rpc("/web/dataset/call_kw/ir.attachment/create", {
            model: "ir.attachment",
            method: "create",
            args: [attachmentValues],
            kwargs: {},
        });
    }
}

Object.assign(GoogleAttachment, {
    template: 'google_attachment.GoogleAttachment',
    props: {
        uploadModel: String,
        uploadId: Number,
    },
});

const _cache = {};

async function getGooglePickerManager() {
    if (!_cache.pickerManager) {
        const params = await fetchConfigParameters();
        const scope = "https://www.googleapis.com/auth/drive";
        const authenticator = new GoogleOAuthAuthenticator(params.clientId, scope)
        _cache.pickerManager = new GooglePickerManager(authenticator, params.apiKey)
    }
    return _cache.pickerManager
}

function fetchConfigParameters() {
    return ajax.rpc("/web/dataset/call_kw/ir.config_parameter/get_google_attachment_parameters", {
        model: "ir.config_parameter", method: "get_google_attachment_parameters", args: [], kwargs: {},
    }).then(function(res){
        if(res.clientId){
            return res
        }
        else {
            throw new Error(
                "Could not load the javascript assets for the module google_attachment. " +
                "The system parameters google_attachment.client_id and google_attachment.api_key " +
                "must be set by the system administrator."
            );
        }
    });
}

return GoogleAttachment;

});
