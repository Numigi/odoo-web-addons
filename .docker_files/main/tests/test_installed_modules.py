# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase


class TestModules(TransactionCase):
    """Test that Odoo modules are installed.

    Because some web modules have no python tests,
    we test that these modules are installed.
    """

    def setUp(self):
        super(TestModules, self).setUp()
        self.modules = self.env['ir.module.module']

    def test_disable_quick_create(self):
        """Quick Create is installed."""
        self.assertTrue(self.modules.search([('name', '=', 'disable_quick_create')]))

    def test_ui_color_red(self):
        """Web UI Red is installed."""
        self.assertTrue(self.modules.search([('name', '=', 'ui_color_red')]))
