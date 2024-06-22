# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from datetime import date,datetime,time,timedelta
# import pytz

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sh_dob=fields.Date(string='Date of Birth')
    sh_send_sms_count = fields.Integer(string='Sent SMS Count',compute='_compute_action_send_sms_count')
    sh_customer_bool = fields.Boolean(string='SMS Customer',default=False)
    
    def _compute_action_send_sms_count(self):
        for rec in self:
            contact_sms_count = self.env['sh.sms.history'].search_count([('sh_partner_id','=',rec.id)])

            rec.sh_send_sms_count = contact_sms_count

    # WISHING TODAY BIRTDAY SMS SEND METHOD 
    @api.model
    def wish_birthday(self):
        today = date.today()
        print('\n\n\n <----------Today Date-------->',today)
        today = date.today()
        partner_id=self.env['res.partner'].search([('sh_dob','=',today)])
        print('\n\n\n\n <-------partner-------->',partner_id)

    # TIME PERIOD UNDER NOT SALE_ORDER CREATE THAT PARTNER SMS SEND METHOD  
    @api.model
    def store_visit_customer_sms(self):
        day = self.env['res.company'].browse(self.env.company.id).sh_sms_day
        print('\n\n\n\n <----Day---->',day)

        # if day >= 1:

        previous_date = date.today() - timedelta(day)
        print('\n\n\n\n <-----previous_date------>',previous_date)
        new_date_time_object = datetime.combine(previous_date, time(00,00,00))
        # print('\n\n\n <--------previous_date----->',new_date_time_object)

        query ="""
            SELECT partner_id
            FROM sale_order
            WHERE (date_order AT TIME ZONE'utc')::date >= %s 
            GROUP BY partner_id
            """

        parameter = [previous_date]

        self._cr.execute(query, parameter)    

        result = self._cr.dictfetchall()
        print('\n\n\n\n <----------result------------>',result)

        if result:
            partner= [rec.get('partner_id') for rec in result]
            print('\n\n\n <--RESULT----->',partner)
            
            if partner:
                customer_send_msg = self.env["res.partner"].sudo().search([('id','not in',partner),('sh_customer_bool','=',False)])
                print('\n\n\n\n <-------customer_send_msg------->',customer_send_msg)

                if customer_send_msg:
                    customer_bool_update = [rec.write({'sh_customer_bool':True}) for rec in customer_send_msg]

    # IR.ACTION.SERVER METHOD
    def action_sms_text_message(self):
        action = {
            'name': _(' Send SMS Text Message'),
            'res_model': 'sh.sms.text.message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }

        return action

    # SMS HISTORY METHOD 
    def sh_sms_history(self):
        
        action= {
            'name': _(' SMS History'),
            'res_model': 'sh.sms.history',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'target':'inline',
            # 'context':{'default_partner_id':self.id},
            # 'domain':"[('sh_partner_id','=',context.get('default_partner_id'))]",
            'domain':[('sh_partner_id','=',self.id)]
        }  
        print(action)

        return action  

    # SEND SMS METHOD 
    def sh_send_sms(self):
        print('\n\n\n self',self)

        action = {
            'name': _(' Send SMS Text Message'),
            'res_model': 'sh.sms.text.message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }
    
        return action

    # Details Loyalty Point METHOD
    def sh_details_loyalty_points(self):
        print('\n\n\n self',self)

        action = {
            'name': _(' Details Loyalty Point'),
            'res_model': 'sh.loyalty.point',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
        }
    
        return action