# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from ddt import data, ddt
from lxml import etree
from odoo.tests import common


MODIFIERS = (
    'invisible',
    'readonly',
    'required',
    'force_save',
)


def _extract_modifier_value(el, modifier):
    return json.loads(el.attrib.get('modifiers') or "{}").get(modifier)


@ddt
class TestViewRendering(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = cls.env.ref('base.view_partner_form')
        cls.email_modifier = cls.env['web.custom.modifier'].create({
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'email',
            'modifier': 'invisible',
        })

        cls.xpath = "//field[@name='street']"
        cls.street_modifier = cls.env['web.custom.modifier'].create({
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'xpath',
            'reference': cls.xpath,
            'modifier': 'invisible',
        })

        cls.hidden_option = 'other'
        cls.env['web.custom.modifier'].create({
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'type',
            'modifier': 'selection_hide',
            'key': cls.hidden_option,
        })

    def _get_rendered_view_tree(self):
        arch = self.env['res.partner'].fields_view_get(view_id=self.view.id)['arch']
        return etree.fromstring(arch)

    @data(*MODIFIERS)
    def test_field_modifier(self, modifier):
        self.email_modifier.modifier = modifier
        tree = self._get_rendered_view_tree()
        el = tree.xpath("//field[@name='email']")[0]
        assert _extract_modifier_value(el, modifier) is True

    @data(*MODIFIERS)
    def test_xpath_modifier(self, modifier):
        self.street_modifier.modifier = modifier
        tree = self._get_rendered_view_tree()
        el = tree.xpath("//field[@name='street']")[0]
        assert _extract_modifier_value(el, modifier) is True

    def test_selection_hide__fields_view_get(self):
        fields = self.env['res.partner'].fields_view_get(view_id=self.view.id)['fields']
        options = {i[0]: i[1] for i in fields['type']['selection']}
        assert self.hidden_option not in options

    def test_selection_hide__fields_get(self):
        fields = self.env['res.partner'].fields_get()
        options = {i[0]: i[1] for i in fields['type']['selection']}
        assert self.hidden_option not in options
