# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

{
    'name': 'Disable Quick Create',
    'version': '1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Web',
    'summary': 'Disable "quick create" for all and "create and edit" '
               'for specific models',
    'depends': ['web'],
    'data': [
        'views/disable_quick_create.xml',
        'views/ir_model.xml',
    ],
    'installable': True,
}
