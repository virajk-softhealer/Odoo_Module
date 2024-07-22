# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from markupsafe import Markup
from odoo.exceptions import UserError

class ShStoreWiseSMSAllocation(models.Model):
    _name = 'sh.store.wise.sms.allocation'
    _description = "Store Wise SMS Allocation"
                
    
    sh_twilio_account_id = fields.Many2one(
        string='Account Reference',
        comodel_name='sh.twilio.account',
        ondelete='cascade',
    )
    sh_store_id = fields.Many2one('sh.client.shop',string='Store')
    sh_allocated_sms = fields.Integer(string='Allocated SMS')
    sh_sent_sms = fields.Integer(string='Sent SMS',compute='_compute_sent_and_remaining_sms')
    sh_remaining_sms = fields.Integer(string='Remaining SMS',compute='_compute_sent_and_remaining_sms')
    # is_boolean = fields.Boolean(string='Is_True',compute='_compute_sent_and_remaining_sms')

     # COMPUTE METHOD 
    @api.depends('sh_sent_sms','sh_remaining_sms')
    def _compute_sent_and_remaining_sms(self):

        for rec in self:
            rec.sh_sent_sms = False
            rec.sh_remaining_sms = False
            
            if rec.sh_store_id:
                total_sent_sms = self.env['sh.sms.history'].search_count([('sh_store_id','=',rec.sh_store_id.id),('sh_state','=','sent')])
                rec.sh_sent_sms = total_sent_sms
                rec.sh_remaining_sms = rec.sh_allocated_sms - rec.sh_sent_sms

    @api.onchange('sh_allocated_sms')
    def onchange_allocated_sms(self):
        
        for rec in self:
            if  rec.sh_twilio_account_id and rec.sh_twilio_account_id.sh_sms_allocation_line:
                total_sms = sum([i.sh_allocated_sms for i in rec.sh_twilio_account_id.sh_sms_allocation_line])
                
                if rec.sh_twilio_account_id.sh_total_allocated_sms < total_sms:
                    raise UserError(_(f"Allocated SMS should not exceed the total allocated SMS. \n"
                    f"Total Allocated SMS : {rec.sh_twilio_account_id.sh_total_allocated_sms} \n"
                    f"Allocated SMS : {total_sms} \n"
                    ))

    # WRITE METHOD 
    def write(self, vals):
        
        # OLD VALUE GETED
        old_store_id = self.sh_store_id.name
        old_allocated_sms = self.sh_allocated_sms
        # old_sent_sms = self.sh_sent_sms
        # old_remainig_sms = self.sh_remaining_sms

        # SUPER METHOD CALL 
        res = super().write(vals)

        # UPDATED VALUE GETED
        new_store_id = ', '.join(self.sh_store_id.name).replace(" ","").replace(",","") if vals.get('sh_store_id') else 'None'
        new_allocated_sms = ', '.join(str(self.sh_allocated_sms)).replace(" ","").replace(",","") if vals.get('sh_allocated_sms') else 'None'
        # new_sent_sms = ', '.join(str(self.sh_sent_sms)).replace(" ","").replace(",","") if vals.get('sh_sent_sms') else 'None'
        # new_remaining_sms = ', '.join(str(self.sh_remaining_sms)).replace(" ","").replace(",","") if vals.get('sh_remaining_sms') else 'None'

        # STORE FIELD  CHECK 
        if vals.get('sh_store_id'):
            store_body = Markup('''
            <ul class="o_Message_trackingValues mb-0 ps-4">
                <li>
                    <div class="o_TrackingValue d-flex align-items-center flex-wrap mb-1" role="group">
                        <span class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold">%s</span>
                        <i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" role="img" aria-label="Changed"></i>
                        <span class="o_TrackingValue_newValue me-1 fw-bold text-info">%s</span>
                        <span class="o_TrackingValue_fieldName ms-1 fst-italic text-muted">(Store)</span>
                    </div>
                </li>

            </ul>''' % (old_store_id,new_store_id))

        # ALLOCATION_SMS FIELD CHECK 
        if vals.get('sh_allocated_sms'):
            sms_body = Markup('''
            <ul class="o_Message_trackingValues mb-0 ps-4">
                <li>
                    <div class="o_TrackingValue d-flex align-items-center flex-wrap mb-1" role="group">
                        <span class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold">%s</span>
                        <i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" role="img" aria-label="Changed"></i>
                        <span class="o_TrackingValue_newValue me-1 fw-bold text-info">%s</span>
                        <span class="o_TrackingValue_fieldName ms-1 fst-italic text-muted">(Allocated SMS)</span>
                    </div>
                </li>

            </ul>''' % (old_allocated_sms,new_allocated_sms))

        # SEND SMS CHECK 
        # if vals.get('sh_sent_sms'):
        #     send_sms_body = Markup('''
        #     <ul class="o_Message_trackingValues mb-0 ps-4">
        #         <li>
        #             <div class="o_TrackingValue d-flex align-items-center flex-wrap mb-1" role="group">
        #                 <span class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold">%s</span>
        #                 <i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" role="img" aria-label="Changed"></i>
        #                 <span class="o_TrackingValue_newValue me-1 fw-bold text-info">%s</span>
        #                 <span class="o_TrackingValue_fieldName ms-1 fst-italic text-muted">(Sent SMS)</span>
        #             </div>
        #         </li>

        #     </ul>''' % (old_sent_sms,new_sent_sms))

        # REMAINING SMS CHECK 
        # if vals.get('sh_remaining_sms'):
        #     remaining_sms_body = Markup('''
        #     <ul class="o_Message_trackingValues mb-0 ps-4">
        #         <li>
        #             <div class="o_TrackingValue d-flex align-items-center flex-wrap mb-1" role="group">
        #                 <span class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold">%s</span>
        #                 <i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" role="img" aria-label="Changed"></i>
        #                 <span class="o_TrackingValue_newValue me-1 fw-bold text-info">%s</span>
        #                 <span class="o_TrackingValue_fieldName ms-1 fst-italic text-muted">(Remaining SMS)</span>
        #             </div>
        #         </li>

        #     </ul>''' % (old_remainig_sms,new_remaining_sms))

        message = {
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'model': 'sh.twilio.account',
            'res_id': self.sh_twilio_account_id.id,
            # 'record_name': self.name,
        }

        if vals.get('sh_store_id'):
            message['body'] = store_body

        if vals.get('sh_allocated_sms'):
            if vals.get('sh_store_id'):

                # CONCATING BODY FIELD 
                message['body'] +=" "+ sms_body
            else:
                message['body'] = sms_body

        # if vals.get('sh_sent_sms'):
        #     if vals.get('sh_store_id'):

        #         # CONCATING BODY FIELD 
        #         message['body'] +=" "+ sms_body

        #     if vals.get('sh_allocated_sms'):
        #         message['body'] = sms_body


        # MAIL.MESSAGE MODEL IN CREATING RECORD 
        message = self.env['mail.message'].sudo().create(message)

        return res
