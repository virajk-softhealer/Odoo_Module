# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


class ShTwilioAccount(models.Model):
    _name = 'sh.twilio.account'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Twilio Account"
    
    name = fields.Char(string='Name',tracking=True)
    sh_account_sid = fields.Char(string='Account SID')
    sh_auth_token = fields.Char(string='Auth Token')
    sh_total_allocated_sms = fields.Integer(string='Total Allocated SMS',tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Connected'),
    ],default='new', string='State', help='State of Twilio account')
    
    sh_body = fields.Text(string='Body', required=False,
                       help='Body for test message',
                       default='This Message is for testing Twilio Connection')
    
    sh_from_number = fields.Char(string='Your Twilio Phone Number', 
                              help='Twilio account number')

    sh_to_number = fields.Char(string='To',
                            help='Recipient number with country code for '
                                 'testing the connection(It should be '
                                 'added to Verified Caller IDs in Twilio).')

    sh_sms_allocation_line = fields.One2many('sh.store.wise.sms.allocation', 'sh_twilio_account_id', string='SMS Allocation Line',tracking=True)
    password = fields.Char(string='Password',default='$pbkdf2-sha512$600000$UeqdE4KQMsbYOydkbA0hhA$aWVcWGkDM87D.pARrqM7hQSrC.NYqSw6VIzVoLYlNBZFjcQ3zkChokQFhm/NFPIyWJOtfut6flf8DFpcQlaoAQ')

    def sh_account_test_connection(self):
        try:
            messages = Client(self.sh_account_sid,self.sh_auth_token).messages.create(
                body =self.sh_body,
                from_ =self.sh_from_number,
                to = self.sh_to_number
            )
            
            if messages.sid:
                self.write({"state":"confirm"}) 
                message_data = _("Connection Successful!")
                message_type = 'success'
            else:
                message_data = _("Connection Not Successful!")
                message_type = 'warning'

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message_data,
                    'type': message_type,
                    'sticky': True,
                }    
            }

        except TwilioException as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': f"Connection Not Successful! {e}.",
                    'type': 'warning',
                    'sticky': True,
                }
            }

    # BUTTON METHOD 
    def action_total_allocated_sms_change(self): 
        return{
            'name':_('Update Total Allocated SMS'),
            'res_model': 'sh.update.allocated.sms',
            'view_mode':'form',
            'target':'new',
            'type':'ir.actions.act_window',

        }   

    def action_edit_twillo_sms_allocation(self):
        pw = 'bbvejut'

        ctx = self.env.user._crypt_context()

        b = ctx.hash(pw)

        a = self.env.user._crypt_context().verify(
                                pw, 'bbvejut')

        valid, replacement = ctx.verify_and_update('bbvejut', b)
        
        