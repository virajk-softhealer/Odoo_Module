# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "PO Customization",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "summary": "",
    "description": """""",
    "version": "16.0.3",
    "depends": ["purchase","stock","point_of_sale"
    ],
    "application": True,
    "data": [
        'security/ir.model.access.csv',

        'views/purchase_views.xml',
        'views/product_views.xml',
        'views/sh_pos_bool_update_views.xml',
    ],

    "auto_install": False,
    "installable": True,

}
