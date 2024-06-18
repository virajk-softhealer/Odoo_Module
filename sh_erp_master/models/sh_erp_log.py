# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShClientShop(models.Model):
    _name = "sh.erp.log"
    _description = "ERP Logs"
    
    shop_id = fields.Many2one('sh.client.shop', string='Shop', copy=False)
    name = fields.Char('Note')
