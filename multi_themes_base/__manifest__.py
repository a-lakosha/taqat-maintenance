# -*- encoding: utf-8 -*-
{
    'name': "Multi Themes Base",
    'summary': """
        Multi Themes Base
    """,
    'description': """
        Multi Themes Base to contain Multi Themes Base 
    """,
    'author': "Ahmed Lakosha",
    'contributors': [
        "<Islam Hafez>"
        "<Sameh Battah>"
    ],
    'category': 'Website',
    'version': '0.3',
    'depends': ['website', 'website_blog', 'base_address_extended', 'website_hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        # inherited models
        'views/blog_views.xml',
        'views/jobs_views.xml',
        'views/res_company_view.xml',
        # new models
        'views/partner_views.xml',
        'views/programs_views.xml',
        'views/projects_views.xml',
        'views/success_stories_views.xml',
        'views/faqs_views.xml',
        'views/past_alerts_archive.xml',
        'views/testimonials.xml',
        'views/website_team.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'application': False,
    'license': 'LGPL-3',
}
