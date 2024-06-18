# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShTwilioAccount(models.Model):
    _name = 'sh.twilio.account'
    _description = "Twilio Account"
    
    name = fields.Char(string='Name')
    sh_account_sid = fields.Char(string='Account SID')
    sh_auth_token = fields.Char(string='Auth Token')
    sh_total_allocated_sms = fields.Integer(string='Total Allocated SMS')
    state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Connected'),
    ], required=True, default='new', string='State', help='State of Twilio account')

    sh_sms_allocation_line = fields.One2many('sh.store.wise.sms.allocation', 'sh_twilio_account_id', string='SMS Allocation Line')

    def sh_account_test_connection(self):
        pass

