# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class SlideChannel(models.Model):

    _inherit = "slide.channel"

    logo = image = fields.Binary(
        "Image",
        attachment=True,
    )
