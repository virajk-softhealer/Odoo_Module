# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields, _

class ShSMSHistory(models.Model):

    _name = 'sh.sms.history'
    _description = 'SMS History'

    sh_partner_id = fields.Many2one('res.partner',string='Customers')
    sh_store_id = fields.Many2one('sh.pos.session',string='Store(Sent From)')
    sh_message = fields.Text(String='Message')
    sh_state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent')],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default="draft")

