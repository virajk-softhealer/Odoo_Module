# -*- coding: utf-8 -*-

# Part of Softhealer Technologies.

{
    'name': 'Employee Entry Exit Own Checklist',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'license': 'OPL-1',
    'support': 'support@softhealer.com',
    'version': '16.0.1',
    'category': 'Human Resources',
    'summary': """
reminder for user entry app,
notify for user exit module,
employee entry checklist,
employee exit checklist odoo
""",
    'description': """
This module is useful to a list of items required,
things to be done, or
points to be considered, used as a reminder.
reminder for user entry app,
notify for user exit module,
employee entry checklist,
employee exit checklist odoo
""",
    'depends': ['hr', 'sh_message'],
    'data': [
        'security/employee_checklist_security.xml',
        'security/ir.model.access.csv',
        'wizard/sh_import_entry_wizard_views.xml',
        'wizard/sh_import_exit_wizard_views.xml',
        'views/sh_employee_entry_custom_checklist_views.xml',
        'views/sh_employee_exit_custom_checklist_views.xml',
        'views/sh_employee_entry_custom_checklist_template_views.xml',
        'views/sh_employee_exit_custom_checklist_template_views.xml',
        'views/hr_employee_views.xml',
    ],
    'images': ['static/description/background.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': '20',
    'currency': 'EUR',
}
