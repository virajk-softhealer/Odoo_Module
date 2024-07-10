# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields, _

class ShSMSHistory(models.Model):

    _name = 'sh.sms.history'
    _description = 'SMS History'
    _order = 'create_date desc,id desc'  

    sh_partner_id = fields.Many2one('res.partner',string='Customers')
    sh_store_id = fields.Many2one('sh.client.shop',string='Store(Sent From)')
    sh_message = fields.Text(string='Message')
    sh_state = fields.Selection([
        ('draft', 'Draft'),
        ('fail', 'Failed'),
        ('sent', 'Sent')
    ], string="State", help='State of SMS', default="draft")

