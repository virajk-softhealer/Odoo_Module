# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api

class sh_config_vehicles(models.Model):
    _name = "sh.agri.vehicles"
    _description = "about vehicles"
    _rec_name = 'fleet_vehicle_id'

    fleet_vehicle_id = fields.Many2one("fleet.vehicle", string="Fleet Vehicle", required=True)
    # total_vehicle = fields.Integer(string="Total Vehicle", required=True)
    begin_date = fields.Date(string="Begin Date", required=True)
    finish_date = fields.Date(string="Finish Date",required=True)
    description = fields.Text(string="Description")

    
   

   

