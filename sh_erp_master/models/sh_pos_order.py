# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShPosOrder(models.Model):
    _name = "sh.pos.order"
    _description = "Pos Order"

    name = fields.Char(string="Name", copy=False)
    sh_shop_id = fields.Many2one('sh.client.shop', string='Shop', copy=False)
    res_id = fields.Integer(string="Remote POS ID", copy=False)
    # sh_session_id = fields.Integer(string='Session ID', copy=False)
    sh_pos_session_id = fields.Many2one('sh.pos.session', string='Session ID')
    date_order = fields.Datetime('Date')
    partner_id = fields.Many2one('res.partner', string='Customer')
    sh_pos_order_line = fields.One2many('sh.pos.order.line','sh_pos_order_id', string='POS Order Lines',)
    sh_pos_payment_line = fields.One2many('sh.pos.payment','sh_pos_order_id', string='POS Payment Lines',)
    amount_tax = fields.Float('Taxes')
    amount_total = fields.Float('Total')
    amount_paid = fields.Float('Amount Paid')

class ShPosOrderLine(models.Model):
    _name = "sh.pos.order.line"
    _description = "Pos Order Line"
    
    sh_pos_order_id = fields.Many2one('sh.pos.order', string='POS Order')
    name = fields.Char(string="Line No", copy=False)
    res_id = fields.Integer(string="Remote POS Line ID", copy=False)
    full_product_name = fields.Char('Product Name')
    qty = fields.Float('Quantity')
    price_unit = fields.Float('Price Unit')
    discount = fields.Float('Discount')
    price_subtotal = fields.Float('Price Subtotal')
    price_subtotal_incl = fields.Float('Price Subtotal Incl')
    
