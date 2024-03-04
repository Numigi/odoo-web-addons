# Copyright 2023 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Google Drive Attachment",
    "version": "1.0.1",
    "category": "Document Management",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "depends": ["base_setup", "mail"],
    "data": [
        "views/assets.xml",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        "static/src/components/google_attachment.xml",
        "static/src/components/attachment_box.xml",
    ],
    "installable": True,
}
