# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShCropConditions(models.Model):
    _name = "sh.crop.condition"
    _description = "Season"

    name = fields.Char(string="Name", required=True)
    qty = fields.Float(string="Value")
    uom_id = fields.Many2one('uom.uom')

    sh_agri_crops_id = fields.Many2one("sh.agriculture.crops")