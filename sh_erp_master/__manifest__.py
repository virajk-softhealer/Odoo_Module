# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "ERP Master",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["base", "base_setup","point_of_sale"],
    "application": True,
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        
        # DATA
        "data/sh_erp_master_dashboard.xml",
        
        # VIEWS
        "views/sh_client_shop_views.xml",

        "views/sh_pos_order_views.xml",
        # "views/sh_pos_payment_views.xml"

    ],
    'assets': {
        'web.assets_backend': [
            # 'sh_erp_master/static/src/js/sh_erp_master_dashboard.js',
            # 'sh_erp_master/static/src/xml/sh_erp_master_dashboard_templates.xml',
            'sh_erp_master/static/src/js/erp_master_dashboard.js',
            'sh_erp_master/static/src/xml/erp_master_dashboard_templates.xml',
            'sh_erp_master/static/src/scss/dashboard.css',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
