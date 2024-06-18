# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    sh_shop_id = fields.Many2one('sh.client.shop', string='Shop')
    res_id = fields.Integer("Remote Customer ID")
