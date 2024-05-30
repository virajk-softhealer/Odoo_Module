# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api



class sh_incident_crops(models.Model):
    _name = "sh.incident.crops"
    _description = "process equipment"

    name = fields.Char(string="Name", required=True)
    crop_name_id = fields.Many2one("sh.agriculture.crops",string="Crop Name", required=True)
    # location_name_id = fields.Many2one("stock.location",string="Location Name")
    # location_name_id = fields.Many2one("res.partner", string="Location Name",
    #                                    domain=[('farm_location', "=", True)])
    task_name = fields.Many2one("sh.list.process", string="Task Name")
    incident_date = fields.Date(string="Incident Date")
    description = fields.Text(string="Description")
