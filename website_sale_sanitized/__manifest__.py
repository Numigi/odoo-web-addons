# Copyright 2019 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Sale Sanitized',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'website': 'https://github.com/OCA/website',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'Sanitize the XML views of the eCommmerce application',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/30_day_money_back.xml',
    ],
    'installable': True,
    'auto_install': True,
}
