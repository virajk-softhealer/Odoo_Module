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
    "depends": ["contacts","sh_erp_master","sale_management","base",
    ],
    "application": True,
    "data": [
        'data/ir_cron_data.xml',
        'data/ir_action_data.xml',
        'security/ir.model.access.csv',

        'wizard/sh_sms_text_message_views.xml',
        'wizard/sh_loyalty_point_views.xml',

        'views/res_config_settings_views.xml',
        'views/sh_twilio_acccount_views.xml',   
        'views/sh_sms_history_views.xml',
        'views/res_partner_views.xml',
        'views/sh_sms_menus.xml',
    ],
    "demo": [
        'demo/sms_demo.xml',
    ],
    "auto_install": False,
    "installable": True,

}
