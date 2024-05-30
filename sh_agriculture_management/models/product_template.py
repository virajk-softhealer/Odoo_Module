# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_agri = fields.Boolean(string="Is Agri")
    agri_crop = fields.Boolean(string="Agri Crop")
    crop_raw_material = fields.Boolean(string="Crop Raw Material")
    # crop_labour = fields.Boolean(string="Crop Labour")
    # crop_overhead = fields.Boolean(string="Crop Overhead")
