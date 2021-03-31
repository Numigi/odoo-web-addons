odoo.define('google_attachment/static/src/components/attachment_box.js', function (require) {
'use strict';

const AttachmentBox = require('mail/static/src/components/attachment_box/attachment_box.js')
const GoogleAttachment = require('google_attachment/static/src/components/google_attachment.js')

Object.assign(AttachmentBox.components, { GoogleAttachment });

});
