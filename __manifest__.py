# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        A real estate module where one can add properties info 
        for advertising purposes""",

    'description': """
        A real estate module where one can add properties info 
        for advertising purposes
    """,

    'author': "Shahin",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_map'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/realestate_views.xml',
        'views/realestateusers_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
