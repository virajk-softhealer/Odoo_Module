# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api

class sh_config_agri_farmers(models.Model):
    _inherit = "res.partner"
    _description = "this model for agriculture farmer, Location and Animal"

    farmer = fields.Boolean(string="Farmer")
    # farm_location = fields.Boolean(string="Farm Location")
    animal = fields.Boolean(string="Animal")
    animal_description = fields.Text("Animal Description")
