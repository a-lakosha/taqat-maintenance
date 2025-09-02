# -*- coding: utf-8 -*-
{
    'name': 'Website Service',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Manage and display services on your website',
    'description': """
        Website Service Module
        ======================
        This module allows you to:
        - Create and manage services
        - Organize services by types and tags
        - Display services on website with professional layout
        - SEO optimization for service pages
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/website_service_security.xml',
        'views/website_service_views.xml',
        'views/website_service_type_views.xml',
        'views/website_service_tag_views.xml',
        'views/website_service_menu.xml',
        'views/service_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_service/static/src/scss/service.scss',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}