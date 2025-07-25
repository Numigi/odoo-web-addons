# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Web Custom Label',
    'version': '14.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Enable easily customizing view labels.',
    'depends': ['base'],
    'data': [
        'views/custom_label.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
