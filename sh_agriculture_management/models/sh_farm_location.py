# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api,Command


class ShFarmLocation(models.Model):
    _name = "sh.farm.location"
    _description = "Farm Location"
    _rec_name = "sh_location"

    sh_location = fields.Char(string="Location", required=True)
    sh_location_size = fields.Float(string='Size', required=True)
    sh_location_size_value = fields.Char(default="Hectare", readonly=True)
    sh_location_address = fields.Text(string="Address")
    sh_soil_id = fields.Many2one('sh.soil', string="Soil")

    # Land Details
    sh_rainfall = fields.Float(string="Rainfall")
    sh_rainfall_uom = fields.Char(default="Inch", readonly=True)
    # sh_rainfall_id = fields.Many2one('uom.uom', string="UoM")
    sh_avrage_summer_temp = fields.Float(string="Summer Temp")
    sh_avrage_summer_temp_uom = fields.Char(default="C", readonly=True)
    # sh_avrage_summer_temp_id = fields.Many2one('uom.uom', string="UoM temp")
    sh_avrage_winter_temp = fields.Float(string="Winter Temp")
    # sh_avrage_winter_temp_id = fields.Many2one('uom.uom', string="UoM temp")
    sh_moisture_content = fields.Float(string="Winter Temp")
    sh_moisture_content_id = fields.Char(default='%', readonly=True)
    sh_avrage_sunlight_day_per_year = fields.Integer(required=True)
    sh_avrage_sunlight_day_per_year_id = fields.Char(
        default='Days', readonly=True)
    sh_water_availibility = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Water Availibility', default='excellent')
    sh_electricity_availibility = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Electricity Availibility', default='excellent')
    sh_distance_from_any_market = fields.Selection([
        ('near', 'Near'),
        ('far', 'Far'),
        ('too far', 'Too Far')
    ], string='Distance From Any Market', default='near')
    sh_distance_from_your_designated_godown = fields.Selection([
        ('near', 'Near'),
        ('far', 'Far'),
        ('too far', 'Too Far')
    ], string='Distance From Your Designated Godown', default='near')
    sh_land_description = fields.Html(string="Description")


    sh_yield_capacity_ids = fields.One2many('sh.yield.capacity','sh_farm_location_id')

    # product_id = fields.Many2one('product.product',string='Crop')
    # sh_yield_meter = fields.Integer()
    # sh_yield_meter_uom_id = fields.Many2one('uom.uom')
    # sh_hectare_to_meter = fields.Integer()
    # sh_total_yield = fields.Integer()
    # sh_total_yield_uom_id = fields.Many2one('uom.uom')


    # Yield Reset Btn 
    def yield_reset_crop_quantity(self):

        if self.sh_yield_capacity_ids:
            for rec in self.sh_yield_capacity_ids:
                self.write({'sh_yield_capacity_ids':[
                    Command.update(rec.id,{'sh_remaining_yield_capacity':rec.sh_total_yield})
                ]})