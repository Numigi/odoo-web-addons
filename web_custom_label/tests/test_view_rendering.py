# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import data, ddt
from lxml import etree
from odoo.tests import common

EN_NAME_LABEL = 'My Custom Label'
FR_NAME_LABEL = 'Mon Libellé Personnalisé'

EN_XPATH_LABEL = 'My Other Custom Label'
FR_XPATH_LABEL = 'Mon Autre Libellé Personnalisé'

EN_NAME_PLACEHOLDER = 'My Custom Placeholder'
FR_NAME_PLACEHOLDER = 'Mon Placeholder Personnalisé'

EN_STREET_LABEL = 'My Custom Street Label'
FR_STREET_LABEL = 'Mon Libellé de Rue Personnalisé'


@ddt
class TestViewRendering(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref('base.lang_fr').write({'active': True})

        cls.view = cls.env.ref('base.view_partner_form')
        cls.env['web.custom.label'].create({
            'lang': 'en_US',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'name',
            'term': EN_NAME_LABEL,
            'position': 'string',
        })

        cls.env['web.custom.label'].create({
            'lang': 'fr_FR',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'name',
            'term': FR_NAME_LABEL,
            'position': 'string',
        })

        cls.xpath = "//field[@name='email']"

        cls.env['web.custom.label'].create({
            'lang': 'en_US',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'xpath',
            'reference': cls.xpath,
            'term': EN_XPATH_LABEL,
            'position': 'string',
        })

        cls.env['web.custom.label'].create({
            'lang': 'fr_FR',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'xpath',
            'reference': cls.xpath,
            'term': FR_XPATH_LABEL,
            'position': 'string',
        })

        cls.env['web.custom.label'].create({
            'lang': 'en_US',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'name',
            'term': EN_NAME_PLACEHOLDER,
            'position': 'placeholder',
        })

        cls.env['web.custom.label'].create({
            'lang': 'fr_FR',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'name',
            'term': FR_NAME_PLACEHOLDER,
            'position': 'placeholder',
        })

        cls.env['web.custom.label'].create({
            'lang': 'en_US',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'street',
            'term': EN_STREET_LABEL,
            'position': 'string',
        })

        cls.env['web.custom.label'].create({
            'lang': 'fr_FR',
            'model_ids': [(4, cls.env.ref('base.model_res_partner').id)],
            'type_': 'field',
            'reference': 'street',
            'term': FR_STREET_LABEL,
            'position': 'string',
        })

        cls.env = cls.env(user=cls.env.ref('base.user_demo'))
        cls.env.user.lang = 'en_US'

    def _get_rendered_view_tree(self, lang):
        arch = (
            self.env['res.partner'].with_context(lang=lang)
            .fields_view_get(view_id=self.view.id)
        )['arch']
        return etree.fromstring(arch)

    @data(
        (None, EN_NAME_LABEL),
        ('en_US', EN_NAME_LABEL),
        ('fr_FR', FR_NAME_LABEL),
    )
    def test_field_node_string(self, data):
        lang, label = data
        tree = self._get_rendered_view_tree(lang=lang)
        el = tree.xpath("//field[@name='name']")[0]
        assert el.attrib.get('string') == label

    @data(
        (None, EN_XPATH_LABEL),
        ('en_US', EN_XPATH_LABEL),
        ('fr_FR', FR_XPATH_LABEL),
    )
    def test_field_node_string_with_xpath(self, data):
        lang, label = data
        tree = self._get_rendered_view_tree(lang=lang)
        el = tree.xpath(self.xpath)[0]
        assert el.attrib.get('string') == label

    @data(
        (None, EN_STREET_LABEL),
        ('en_US', EN_STREET_LABEL),
        ('fr_FR', FR_STREET_LABEL),
    )
    def test_label_node_string(self, data):
        """If any label node related to the field, it is overriden by the custom label.

        For example, if we have:

        <label for="street" string="Address">
        <div>
            <div class="o_address_format" name="div_address">
                <field name="street" ...
            </div>
        </div>

        A custom label referencing the field street should be applied on the label node as well.
        """
        lang, label = data
        tree = self._get_rendered_view_tree(lang=lang)
        el = tree.xpath("//label[@for='street']")[0]
        assert el.attrib.get('string') == label

    @data(
        (None, EN_NAME_PLACEHOLDER),
        ('en_US', EN_NAME_PLACEHOLDER),
        ('fr_FR', FR_NAME_PLACEHOLDER),
    )
    def test_placeholder(self, data):
        lang, label = data
        tree = self._get_rendered_view_tree(lang=lang)
        el = tree.xpath("//field[@name='name']")[0]
        assert el.attrib.get('placeholder') == label

    @data(
        (None, EN_NAME_LABEL),
        ('en_US', EN_NAME_LABEL),
        ('fr_FR', FR_NAME_LABEL),
    )
    def test_label_is_updated_in_fields_view_get(self, data):
        lang, label = data
        fields = (
            self.env['res.partner'].with_context(lang=lang)
            .fields_view_get(view_id=self.view.id)
        )['fields']
        assert fields['name']['string'] == label

    @data(
        (None, EN_NAME_LABEL),
        ('en_US', EN_NAME_LABEL),
        ('fr_FR', FR_NAME_LABEL),
    )
    def test_label_is_updated_in_fields_get(self, data):
        lang, label = data
        fields = self.env['res.partner'].with_context(lang=lang).fields_get()
        assert fields['name']['string'] == label
