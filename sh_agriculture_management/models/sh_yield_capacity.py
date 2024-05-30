# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class ShYieldCapacity(models.Model):
    _name = "sh.yield.capacity"
    _description = "About Yield Capacity"

    product_id = fields.Many2one('product.product',string='Crop')
    sh_yield_meter = fields.Float()
    sh_yield_meter_uom = fields.Char(string="Unit of Measure",default ='KG/M2', readonly=True)
    # sh_yield_meter_uom_id = fields.Many2one('uom.uom')
    sh_hectare_to_meter = fields.Float()
    sh_total_yield = fields.Float()
    sh_total_yield_meter_uom = fields.Char(string="Unit of Measure",default ='KG', readonly=True)
    sh_remaining_yield_capacity = fields.Float()

    sh_farm_location_id = fields.Many2one('sh.farm.location')


    # def _compute_sh_hectare_to_meter(self):
    #     for rec in self:
    #         rec.sh_hectare_to_meter = 0
    #         if rec.sh_farm_location_id.sh_location_size:
    #             rec.sh_hectare_to_meter = rec.sh_farm_location_id.sh_location_size * 10000

    # compute="_compute_sh_total_yield"
    # def _compute_sh_total_yield(self):
    #     for rec in self:
    #         rec.sh_total_yield = 0
    #         if rec.sh_yield_meter and rec.sh_hectare_to_meter:
    #             rec.sh_total_yield = rec.sh_yield_meter * rec.sh_hectare_to_meter

    @api.onchange("sh_yield_meter")
    def onchange_sh_yield_meter(self):
        for rec in self:
            rec.sh_total_yield = 0
            if rec.sh_yield_meter and rec.sh_hectare_to_meter:
                rec.sh_total_yield = rec.sh_yield_meter * rec.sh_hectare_to_meter
            if rec.sh_total_yield:
                rec.sh_remaining_yield_capacity = rec.sh_total_yield
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['sh_farm_location_id']:
                farm = self.env['sh.farm.location'].browse(vals['sh_farm_location_id'])
                vals['sh_hectare_to_meter'] = farm.sh_location_size * 10000
            if vals['sh_yield_meter'] and vals['sh_hectare_to_meter']:
                vals['sh_total_yield'] = vals['sh_yield_meter'] * vals['sh_hectare_to_meter']
            if vals['sh_total_yield']:
                vals['sh_remaining_yield_capacity'] = vals['sh_total_yield']
        
        return super(ShYieldCapacity, self).create(vals_list)
        