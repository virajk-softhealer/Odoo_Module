# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_auto_birth_remainder = fields.Boolean(string='Auto Birthday Reminder')
    sh_auto_visit_remainder = fields.Boolean(string='Auto Store Visit Reminder')
    sh_birthday_sms_temp_id = fields.Many2one('sms.template', string='Birthday SMS Template')
    sh_store_visit_sms_temp_id = fields.Many2one('sms.template', string='Store Visit SMS Template')
    sh_sms_day = fields.Integer(string='Send sms after days of last order')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_auto_birth_remainder = fields.Boolean(string='Auto Birthday Reminder',related='company_id.sh_auto_birth_remainder',readonly=False)
    sh_auto_visit_remainder = fields.Boolean(string='Auto Store Visit Reminder',related='company_id.sh_auto_visit_remainder',readonly=False)
    sh_birthday_sms_temp_id = fields.Many2one(string='Birthday SMS Template',related='company_id.sh_birthday_sms_temp_id',readonly=False)
    sh_store_visit_sms_temp_id = fields.Many2one(string='Store Visit SMS Template',related='company_id.sh_store_visit_sms_temp_id',readonly=False)
    sh_sms_day = fields.Integer(string='Send sms after days of last order',related='company_id.sh_sms_day',readonly=False)
    
