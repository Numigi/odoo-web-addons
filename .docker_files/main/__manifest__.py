# © 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'disable_quick_create',
        # 'google_attachment',
        'web_custom_label',
        'web_custom_modifier',
        'web_contextual_search_favorite',
        'web_editor_backend_context',
        'web_form_disable_autocomplete',
        'web_handle_condition',
        'web_list_column_width',
        'web_trash_condition',
        # 'website_google_analytics_fixed',
        #'website_blog_internal',
        'website_landing_template',
        'website_menu_by_user_status',
    ],
    'installable': True,
}
