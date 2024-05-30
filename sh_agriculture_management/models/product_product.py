# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_agri = fields.Boolean(
        string="Is Agri", related='product_tmpl_id.is_agri',readonly=False)
    agri_crop = fields.Boolean(
        string="Agri Crop", related='product_tmpl_id.agri_crop', readonly=False)
    crop_raw_material = fields.Boolean(
        string="Crop Raw Material", related='product_tmpl_id.crop_raw_material', readonly=False)
    # crop_labour = fields.Boolean(
    #     string="Crop Labour", related='product_tmpl_id.crop_labour', readonly=False)
    # crop_overhead = fields.Boolean(
    #     string="Crop Overhead", related='product_tmpl_id.crop_overhead', readonly=False)
