# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from datetime import timedelta, datetime

class sh_crop_request(models.Model):
    _name = "sh.crop.request"
    _description = "Crop Request Wizard"

    request_crop_id = fields.Many2one("sh.crop.request.wizard")

    partner_id = fields.Many2one("res.partner", string="Name")
    user_id = fields.Many2one(
        "res.users", string="Superviser", default=lambda self: self.env.user)
    being_date = fields.Date(string="Start Date")
    finish_date = fields.Date(string="Finish Date")
    sh_agriculture_crops_id = fields.Many2one(
        'sh.agriculture.crops', string="Crop")
    farmer_id = fields.Many2one("res.partner", string="Farmer",
                                domain=[('farmer', '=', True)])
    estimated_quantity = fields.Float(string="Estimated Quantity")

    crop_uom_id = fields.Many2one('uom.uom',string="UoM")

    sh_farm_location_id = fields.Many2one('sh.farm.location')
    sh_yeild_capacity = fields.Float()
    
    sh_remaining_yield_capacity = fields.Float()
    
    sale_order_id = fields.Many2one('sale.order', string="Related Sale Order")
    


    @api.onchange('being_date')
    def _onchange_dates(self):        
        self.finish_date = self.being_date + timedelta(days=self.sh_agriculture_crops_id.sh_crops_duration) if self.being_date and self.sh_agriculture_crops_id.sh_crops_duration else  False

    
    @api.onchange('sh_farm_location_id')
    def _onchange_sh_farm_location_id(self):
        for rec in self:
            for res in rec.sh_farm_location_id.sh_yield_capacity_ids:
                if rec.sh_agriculture_crops_id.product_id == res.product_id:
                    rec.sh_yeild_capacity = res.sh_total_yield
                    rec.sh_remaining_yield_capacity = res.sh_remaining_yield_capacity - rec.estimated_quantity
                    res.sudo().write({
                        'sh_remaining_yield_capacity' : rec.sh_remaining_yield_capacity
                    })