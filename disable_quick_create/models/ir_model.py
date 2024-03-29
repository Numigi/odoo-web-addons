# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):

    _inherit = 'ir.model'

    disable_create_edit = fields.Boolean('Disable the Create and Edit option')
