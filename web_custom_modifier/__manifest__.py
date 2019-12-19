# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Web Custom Modifier',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Enable easily customizing view modifiers.',
    'depends': ['base'],
    'data': [
        'views/web_custom_modifier.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
