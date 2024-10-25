# -*- coding: utf-8 -*-
{
    "name": "Training Odoo",
    "summary": """ Modul untuk latihan technical Odoo """,
    "description": """
        Modul ini berfungsi untuk mempraktekan technical documentation pada website resmi odoo.com. Sebagian hal yang akan dipelajari adalah :
        - ORM
        - Berbagai View
        - Report
        - Wizard
        - Dll
    """,
    "author": "PT. Ismata Nusantara Abadi",
    "website": "https://www.ismata.co.id",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "product", "mail", "sales_team", "sale", "report_xlsx"],
    # always loaded
    "data": [
        "report/report_training_session.xml",
        "report/report_action.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sequence_data.xml",
        "views/scheduler_data.xml",
        "views/views.xml",
        "views/partner_views.xml",
        "wizard/training_wizard_views.xml",
        "views/menuitems.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "aplication": True,
    "installable": True,
    # "auto_install": False,
}
