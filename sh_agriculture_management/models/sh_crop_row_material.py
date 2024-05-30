# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_crop_row_material(models.Model):
    _name = "sh.crop.row.material"
    _description = "crops row material"



    product_id = fields.Many2one(
        'product.product', string="Product", required=True)
    name = fields.Char()
    description = fields.Text(string="Description",
                              compute='_compute_name',
                              store=True, readonly=False, required=True, precompute=True)
    quantity = fields.Integer(string="Qunatity")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', depends=[
                                              'product_id'], string="Unit of Measure")

    sh_agri_crops_id = fields.Many2one("sh.agriculture.crops")
   

    @api.depends('product_id')
    def _compute_name(self):
        for line in self:
            if not line.product_id:
                continue
            else :
                for rec in line.product_id:
                        line.description = rec.name
                      
