# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _


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
        print("Hello VIRAJ")