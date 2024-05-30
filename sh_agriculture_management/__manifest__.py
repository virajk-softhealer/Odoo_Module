# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "sh Agriculture Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "summary": "sh Agriculture Management",
    "description": """sh Agriculture Management""",
    "version": "16.0.3",
    "depends": ["base", "sale","sale_management","stock","contacts", "fleet", 
                "maintenance","project",],
    "application": True,
    "data": [
        "security/sh_agriculture_security.xml",
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        #wizard
        "wizard/sh_crop_request_wizard_views.xml",
        "wizard/sh_less_qty_reason_views.xml",
        
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/sh_config_agri_farmers_views.xml",
        "views/sh_config_vehicles_views.xml",
        "views/sh_agriculture_crops_views.xml",
        "views/sh_list_process_views.xml",
        "views/sh_diseaes_crops_views.xml",
        "views/sh_incident_crops_views.xml",
        "views/sh_crop_orders_views.xml",
        "views/sale_order_views.xml",
        "views/sh_process_equiment_views.xml",
        "views/sh_process_vehicles_views.xml",
        "views/sh_process_animal_views.xml",
        "views/project_views.xml",
        "views/sh_season_views.xml",
        "views/sh_farm_location_views.xml",
        "views/sh_soil_views.xml",
        "views/sh_labour_views.xml",
        "views/sh_agriculture_menuitems.xml",

  
        # Reports
        'report/ir_actions_report.xml',
        'report/sh_crop_orders_report.xml',
        'report/sh_agriculture_crops_report.xml',
    ],

    "auto_install": False,
    "installable": True,

}
