# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Shopinvader client',
    'description': """Base machinery for odoo shopinvader client""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp SA',
    'depends': [
        'website',
        "base_rest",
        "auth_api_key",
    ],
    'data': [
        'views/website_views.xml',
        'views/website_settings_views.xml',
    ],
}
