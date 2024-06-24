# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from markupsafe import Markup


class ShStoreWiseSMSAllocation(models.Model):
    _name = 'sh.store.wise.sms.allocation'
    _description = "Store Wise SMS Allocation"
                
    
    sh_twilio_account_id = fields.Many2one(
        string='Account Reference',
        comodel_name='sh.twilio.account',
        ondelete='cascade',
    )
    sh_store_id = fields.Many2one('sh.pos.session',string='Store')
    sh_allocates_sms = fields.Integer(string='Allocated SMS')
    
    # WRITE METHOD 
    def write(self, vals):
        
        # OLD VALUE GETED
        old_store_id = self.sh_store_id.name
        old_allocated_sms = self.sh_allocates_sms

        # SUPER METHOD CALL 
        res = super().write(vals)

        # UPDATED VALUE GETED
        new_store_id = ', '.join(self.sh_store_id.name).replace(" ","").replace(",","") if vals.get('sh_store_id') else 'None'
        new_allocated_sms = ', '.join(str(self.sh_allocates_sms)).replace(" ","").replace(",","") if vals.get('sh_allocates_sms') else 'None'

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
        if vals.get('sh_allocates_sms'):
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

        
        message = {
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'model': 'sh.twilio.account',
            'res_id': self.sh_twilio_account_id.id,
            # 'record_name': self.name,
        }

        if vals.get('sh_store_id'):
            message['body'] = store_body

        if vals.get('sh_allocates_sms'):
            if vals.get('sh_store_id'):

                # CONCATING BODY FIELD 
                message['body'] +=" "+ sms_body
            else:
                message['body'] = sms_body

        # MAIL.MESSAGE MODEL IN CREATING RECORD 
        message = self.env['mail.message'].sudo().create(message)
        # print('\n\n\n\n <------------message>',message)

        return res
