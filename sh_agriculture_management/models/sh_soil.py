# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShSoil(models.Model):
    _name = "sh.soil"
    _description = "Soil"


    name = fields.Char(string="Soil", required=True)
    soil_description = fields.Text(string="Description")

    sh_agri_crops_id = fields.Many2one("sh.agriculture.crops")