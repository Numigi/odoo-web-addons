# Copyright 2017 Savoir-faire Linux
# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

{
    "name": "Disable Quick Create",
    "version": "16.0.1.0.0",
    "author": "Savoir-faire Linux",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Web",
    "summary": 'Disable "quick create" for all and "create and edit" '
    "for specific models",
    "depends": ["web"],
    "data": [
        "views/ir_model.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "disable_quick_create/static/src/js/disable_quick_create.js",
        ],
    },
    "installable": True,
}
