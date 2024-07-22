# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models,fields, _ 

class PosCategory(models.Model):
    _inherit = "pos.category"

    sh_deduct_percentage = fields.Float(string='Deduct Total sales (%) in dashboard')
