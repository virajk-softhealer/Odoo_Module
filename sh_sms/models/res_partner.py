# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from datetime import date,datetime,time,timedelta
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sh_dob=fields.Date(string='Date of Birth')
    sh_send_sms_count = fields.Integer(string='Sent SMS Count')
    sh_customer_bool = fields.Boolean(string='SMS Customer',default=False)
    sh_top_store = fields.Many2one('sh.client.shop',string='Top Store')
   
    # WISHING TODAY BIRTDAY SMS SEND METHOD 
    # CRON METHOD 
    @api.model
    def wish_birthday(self):

        customer = self.env['res.partner'].search([('sh_dob','=',fields.Date.today())])
        birthday_sms_template = self.env.company.sh_birthday_sms_temp_id
        twilio_account = self.env['sh.twilio.account'].search([('state','=','confirm')],limit=1)
        
        if not birthday_sms_template:
            #TODO: FIALED SEND SMS DEUT TO MOBILE NUMBER IS NOT SET IN CUSTOMER
            # for rec in customer:
                self.env['sh.sms.history'].create({
                    'sh_message':'Started birthday wishing reminder cron: Birthday SMS template is not defined.',
                    'sh_state':'fail'
                })
                return 

        if not twilio_account:
            #TODO: FIALED SEND SMS DEUT TO MOBILE NUMBER IS NOT SET IN CUSTOMER
            # for rec in customer:
                self.env['sh.sms.history'].create({
                    'sh_message':'Started birthday wishing reminder cron: The twilio account details invalid.',
                    'sh_state':'fail'
                })
                return 
      
        if customer and birthday_sms_template.body and twilio_account:
            client = Client(twilio_account.sh_account_sid,
                twilio_account.sh_auth_token)
                   
            for rec in customer:
                try :
                    if rec.mobile:
                        
                        # RENDER TEMPLATE 
                        body = birthday_sms_template._render_template(birthday_sms_template.body,'res.partner',rec.ids)

                        message = client.messages.create(
                            body= body.get(rec.id),
                            from_=twilio_account.sh_from_number,
                            to=rec.mobile
                        )

                        self.env['sh.sms.history'].create({
                            'sh_partner_id':rec.id,
                            'sh_store_id':rec.sh_top_store.id,
                            'sh_message':body.get(rec.id),
                            'sh_state':'sent'
                        })
                        rec.sh_send_sms_count+=1

                    if not rec.mobile:
                        #TODO: FIALED SEND SMS DEUT TO MOBILE NUMBER IS NOT SET IN CUSTOMER
                        self.env['sh.sms.history'].create({
                            'sh_partner_id':rec.id,
                            'sh_store_id':rec.sh_top_store.id,
                            'sh_message':'Started birthday wishing reminder cron: The mobile number is empty.',
                            'sh_state':'fail'
                        })

                except TwilioException as e:
                    #TODO: FIALED SEND SMS DEUT TO MOBILE NUMBER IS NOT SET IN CUSTOMER
                    self.env['sh.sms.history'].create({
                            'sh_partner_id':rec.id,
                            'sh_store_id':rec.sh_top_store.id,
                            'sh_message':f'Started birthday wishing reminder cron: Twilio account details invalid ..! {e}',
                            'sh_state':'fail'
                        })

    # TIME PERIOD UNDER NOT SALE_ORDER CREATE THAT PARTNER SMS SEND METHOD  
    # CRON METHOD 

    @api.model
    def store_visit_customer_sms(self):
        day = self.env.company.sh_sms_day
        # print('\n\n\n\n DAY',day)

        store_person_sms_template = self.env.company.sh_store_visit_sms_temp_id
        # print('\n\n\n\n STORE_PERSON_SMS',store_person_sms_template)

        twilio_account = self.env['sh.twilio.account'].search([('state','=','confirm')],limit=1)

        # if day >= 1:
        previous_date = date.today() - timedelta(day)
        # print('\n\n\n\n <-----previous_date------>',previous_date)

        query ="""
            SELECT partner_id
            FROM sale_order
            WHERE (date_order AT TIME ZONE'utc')::date >= %s 
            GROUP BY partner_id
            """

        parameter = [previous_date]

        self._cr.execute(query, parameter)    

        result = self._cr.dictfetchall()

        partner =[]        
        if result:
            partner.extend(rec.get('partner_id') for rec in result)
            # print('\n\n\n\n PARTNER',partner)

            if partner and not twilio_account:
                # customer_send_msg = self.env["res.partner"].sudo().search([('id','not in',partner),('sh_customer_bool','=',False)])

                self.env['sh.sms.history'].create({
                    'sh_message':'Started Store vist reminder cron: The twilio account details invalid.',
                    'sh_state':'fail'
                })
                return

            if partner and not store_person_sms_template:
                self.env['sh.sms.history'].create({
                    'sh_message':'Started store visit reminder cron: Store visit template not set in settings.',
                    'sh_state':'fail'
                })
            
                return

            if partner and twilio_account:
                customer_send_msg = self.env["res.partner"].sudo().search([('id','not in',partner),('sh_customer_bool','=',False)])
                client = Client(twilio_account.sh_account_sid,twilio_account.sh_auth_token)

                for rec in customer_send_msg:
                    try:
                        if rec.mobile:
                            body = store_person_sms_template._render_template(store_person_sms_template.body,'res.partner',rec.ids)

                            message = client.messages.create(
                                body= body.get(rec.id),
                                from_=twilio_account.sh_from_number,
                                to=rec.mobile
                            )
                            
                            self.env['sh.sms.history'].create({
                                'sh_partner_id':rec.id,
                                'sh_store_id':rec.sh_top_store.id,
                                'sh_message':body.get(rec.id),
                                'sh_state':'sent'
                            })
                            rec.sh_send_sms_count+= 1
                            rec.sh_customer_bool= True
                        
                        if not rec.mobile:
                            self.env['sh.sms.history'].create({
                                'sh_partner_id':rec.id,
                                'sh_store_id':rec.sh_top_store.id,
                                'sh_message':'Started store visit reminder cron: The mobile number is empty.',
                                'sh_state':'fail'
                            })

                    except TwilioException as e:
                        #TODO: FIALED SEND SMS DEUT TO MOBILE NUMBER IS NOT SET IN CUSTOMER
                        self.env['sh.sms.history'].create({
                            'sh_partner_id':rec.id,
                            'sh_store_id':rec.sh_top_store.id,
                            'sh_message':f'Started store visit reminder cron: Twilio account details invalid ..! {e}',
                            'sh_state':'fail'
                        })
    
    # IR.ACTION.SERVER METHOD
    def action_sms_text_message(self):
        return {
            'name': _(' Send SMS Text Message'),
            'res_model': 'sh.sms.text.message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }

    # SMS HISTORY METHOD 
    def sh_sms_history(self):
        
        return {
            'name': _(' SMS History'),
            'res_model': 'sh.sms.history',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'target':'inline',
            # 'context':{'default_partner_id':self.id},
            # 'domain':"[('sh_partner_id','=',context.get('default_partner_id'))]",
            'domain':[('sh_partner_id','=',self.id)]
        }  

    # SEND SMS METHOD 
    def sh_send_sms(self):
        # print('\n\n\n self',self)
        return {
            'name': _(' Send SMS Text Message'),
            'res_model': 'sh.sms.text.message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }

    # Details Loyalty Point METHOD
    def sh_details_loyalty_points(self):
        # print('\n\n\n self',self)
        return {
            'name': _(' Details Loyalty Point'),
            'res_model': 'sh.loyalty.point',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }
    