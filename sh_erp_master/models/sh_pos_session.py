# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShPosSession(models.Model):
    _name = "sh.pos.session"
    _description = "Pos Session"
    
    name = fields.Char(string="Session", copy=False)
    res_id = fields.Integer(string="Remote Session ID", copy=False)
    sh_pos_order_id = fields.Many2one('sh.pos.order', string='POS Order')
    sh_shop_id = fields.Many2one('sh.client.shop', string='Shop', copy=False)
