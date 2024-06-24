# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Resize Observer Error Catcher",
    "summary": "Skip Resize Observer interface error when zooming.",
    "version": "16.0.1.0.0",
    "website": "https://bit.ly/numigi-com",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "AGPL-3",
    "depends": ["base_setup"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "resize_observer_error_catcher/static/src/js/resize_observer_catcher.js",
        ],
    },
    "installable": True,
}
