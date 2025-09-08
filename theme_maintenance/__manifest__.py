# -*- encoding: utf-8 -*-
{
    'name': "Maintenance",
    'summary': """
        Maintenance Theme for Odoo    """,
    'description': """
        Maintenance Theme 

    """,
    'author': "Ahmed Lakosha",
    'sequence': 1,
    'contributors': [
        "<Ahmed Lakosha>",
        "< Hasnaa Ayman>",
        "<Youssef Hussein >",
    ],
    'category': 'Theme',
    'version': '0.1',
    'depends': ['theme_common', 'social_media', 'mass_mailing', 'website', 'crm', 'website_service',
                'multi_themes_base'],
    'data': [

        'data/pages/home_page.xml',
        'data/pages/about_page.xml',
        'data/pages/contact_page.xml',
        'data/pages/services_page.xml',
        'views/header.xml',
        'views/custom_footer.xml',
    ],
    'images': [
        'static/description/maintenance_description.png',
        'static/description/maintenance_screenshot.png',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_maintenance/static/src/lib/owl-carousel/**/*',
            'theme_maintenance/static/src/lib/bootstrap-icons/bootstrap-icons.css',
            'theme_maintenance/static/src/scss/custom.scss',
            'theme_maintenance/static/src/scss/style1.scss',
            'theme_maintenance/static/src/scss/style2.scss',
            'theme_maintenance/static/src/scss/style3.scss',
            'theme_maintenance/static/src/js/snippets.component.js',
            'theme_maintenance/static/src/js/script.js',

        ],
        'web._assets_primary_variables': [
            'theme_maintenance/static/src/scss/primary_variables.scss',
        ],
    },
    'application': False,
    'license': 'LGPL-3',
}
