# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api,models,fields, _ 
from odoo.exceptions import UserError


class ShUpdateAllocatedSMS(models.TransientModel):
    _name ='sh.update.allocated.sms'
    _description = 'Update Allocated SMS'

    sh_update_total_allocated_sms = fields.Integer(string='Update Total Allocated SMS')
    password = fields.Char(string='Password')   

    # UPDATE ALLOCATED SMS ACTION 
    def action_update_allocated_sms(self):
        
        if self.env.context.get('active_id'):
            twilio_account = self.env['sh.twilio.account'].browse(self.env.context.get('active_id'))

            if twilio_account and twilio_account.password:

                valid, replacement = self.env.user._crypt_context().verify_and_update(self.password,twilio_account.password)

                if not valid:
                    raise UserError (_("The password is wrong."))

                else:
                    twilio_account.sh_total_allocated_sms = self.sh_update_total_allocated_sms
