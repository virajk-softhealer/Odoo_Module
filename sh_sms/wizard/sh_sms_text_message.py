# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api,fields, models, _
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

class ShSMSTextMessage(models.TransientModel):
    _name = 'sh.sms.text.message'
    _description = 'SMS Text Message'
    
    sh_send_message_type = fields.Selection([
        ('template', 'Template'),
        ('custome_message', 'Custom Message')],required=True,default='template')

    sh_sms_template_id =  fields.Many2one('sms.template',string='Select Template')
    sh_custom_message = fields.Text(string='Custom Message')     
  
    # WIZARD THROUGHT SEND MESSAGE 
    def action_send_now(self):
        twilio_account = self.env['sh.twilio.account'].search([('state','=','confirm')],limit=1)
        customer = self.env['res.partner'].sudo().browse(r for r in self.env.context.get('active_ids'))

        if twilio_account and customer:
            
            for rec in customer:
                try :
                    client = Client(twilio_account.sh_account_sid,twilio_account.sh_auth_token)
                    # print('\n\n\n\n CLIENT',client)
                    
                    body = self.sh_sms_template_id._render_template(self.sh_sms_template_id.body,'res.partner',customer.ids)
                    if rec.mobile:
                        # print('\n\n\n MOBILE',rec.mobile)
                        # TEMPLATE 
                        if self.sh_send_message_type =='template' and self.sh_sms_template_id and self.sh_sms_template_id.body:
                            
                            message = client.messages.create(
                                    body= body.get(rec.id),
                                    from_=twilio_account.sh_from_number,
                                    to=rec.mobile
                                )
                            # print('\n\n\n MESSAGE',message)
                            # print('\n\n\n MESSAGE SID',message.sid)

                            sms_history = self.env['sh.sms.history'].create({
                                'sh_partner_id':rec.id,
                                'sh_store_id':rec.sh_top_store.id,
                                'sh_message':body.get(rec.id),
                                'sh_state':'sent'
                            })

                            if sms_history:
                                rec.sh_send_sms_count+=1
                                # sms_history.update({'sh_state':'sent'})

                        # CUSTOME MESSAGE 
                        if self.sh_send_message_type =='custome_message':

                            message = client.messages.create(
                                    body= self.sh_custom_message,
                                    from_=twilio_account.sh_from_number,
                                    to=rec.mobile
                                )
                            sms_history = self.env['sh.sms.history'].create({
                                'sh_partner_id':rec.id,
                                'sh_store_id':rec.sh_top_store.id,
                                'sh_message':self.sh_custom_message,
                                'sh_state':'sent'
                                })

                            if sms_history:
                                rec.sh_send_sms_count+= 1

                    if not rec.mobile:
                        # print("\n\n\n\n HELLO1")
                        message_data = _("Mobile Number Empty!")
                        return{
                            'type':'ir.actions.client',
                            'tag': 'display_notification',
                            'params':{
                                'message':message_data,
                                'type':'warning',
                                'sticky':False,
                                'next':{
                                    'type': 'ir.actions.act_window_close'
                                }
                            }
                        }

                except TwilioException:
                    # print("\n\n\n\n HELLO2")
                    message_data = _("Twilio Credentials Wrong!")
                    return{
                        'type':'ir.actions.client',
                        'tag': 'display_notification',
                        'params':{
                            'message':message_data,
                            'type':'warning',
                            'sticky':False,
                            'next':{
                                'type': 'ir.actions.act_window_close'
                            }
                        }
                    }

        else:
            # print("\n\n\n\n HELLO3")
            message_data = _("Not Twilio Account!")
            return{
                'type':'ir.actions.client',
                'tag': 'display_notification',
                'params':{
                    'message':message_data,
                    'type':'warning',
                    'sticky':False,
                    'next':{
                        'type': 'ir.actions.act_window_close'
                    }
                }
            }