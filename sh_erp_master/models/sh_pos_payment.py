# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShPosPayment(models.Model):
    _name = "sh.pos.payment"
    _description = "Pos Payment"

    sh_pos_order_id = fields.Many2one('sh.pos.order', string='Order Ref')
    # sh_session_id = fields.Integer(related='sh_pos_order_id.sh_session_id')
    sh_pos_session_id = fields.Many2one('sh.pos.session', string='Session ID',related='sh_pos_order_id.sh_pos_session_id')
    name = fields.Char(string="Name", copy=False)
    res_id = fields.Integer(string="Record ID", copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer')
    payment_method = fields.Char(string="Payment Method", copy=False)
    amount = fields.Float(string="Amount", copy=False)
    payment_date = fields.Datetime('Date')
