odoo.define('attachment.DonwloadManager', function (require) {
    "use strict";

const components = {
    Attachment : require('mail/static/src/components/attachment/attachment.js'),
};

const { patch } = require('web.utils');

patch(components.Attachment, 'attachment.DonwloadManager', {
    _onClickDownload(ev) {
        ev.stopPropagation();
        window.open( `/web/content/ir.attachment/${this.attachment.id}/datas?download=true`, "_newtab" );
    }
});
});