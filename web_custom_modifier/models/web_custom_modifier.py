# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, modules, tools


class WebCustomModifier(models.Model):

    _name = 'web.custom.modifier'
    _description = 'Custom View Modifier'

    model_ids = fields.Many2many(
        'ir.model', 'ir_model_custom_modifier', 'modifier_id', 'model_id', 'Model')
    type_ = fields.Selection([
        ('field', 'Field'),
        ('xpath', 'Xpath'),
    ], default='field', required=True)
    modifier = fields.Selection([
        ('invisible', 'Invisible'),
        ('readonly', 'Readonly'),
        ('required', 'Required'),
    ], required=True)
    reference = fields.Char(required=True)
    active = fields.Boolean(default=True)


class WebCustomModifierWithCachedModifiers(models.Model):
    """Add a cache for getting the modifiers.

    The system cache is invalidated when any modifier record is added / modified / deleted.
    """

    _inherit = 'web.custom.modifier'

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return new_record

    @api.multi
    def write(self, vals):
        super().write(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @api.multi
    def unlink(self):
        super().unlink()
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @tools.ormcache('model')
    def _find_modifiers(self, model):
        """Find the modifiers matching the given model.

        :param model: the name of the model.
        :return: a list of custom modifiers values (list of dictionaries)
        """
        return self.sudo().env['web.custom.modifier'].search([
            ('model_ids.model', '=', model),
        ]).read()
