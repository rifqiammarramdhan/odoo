# -*- coding: utf-8 -*-
{
    "name": "travel_umroh",
    "summary": """
        Module untuk melakukan manajemen travel Umroh
    """,
    "description": """
        Travel Umrah Management
    """,
    "author": "Rifqi Ammar Ramadhan",
    "website": "https://rifqiammarramadhan.xyz/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "product", "sale", "mrp"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/partner_view.xml",
        "views/templates.xml",
        "views/menuitems.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "aplication": True,
    "installable": True,
}
