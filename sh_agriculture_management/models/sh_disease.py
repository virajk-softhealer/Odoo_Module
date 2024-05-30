# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_diseaes(models.Model):
    _name = "sh.disease"
    _description = "About Disease"
    _rec_name = 'disease'
    
    disease = fields.Char(string="Disease", required=True)
    details = fields.Text(string="Details")