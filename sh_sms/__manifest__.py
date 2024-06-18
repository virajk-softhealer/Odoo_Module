# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Twilio SMS Notifications",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["base","contacts","sh_erp_master"
    ],
    "application": True,
    "data": [
        'security/ir.model.access.csv',

        'views/sh_twilio_acccount_views.xml',

        'views/sh_sms_menus.xml',
    ],

    "auto_install": False,
    "installable": True,

}
