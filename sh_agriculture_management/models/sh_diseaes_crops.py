# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_diseaes_crops(models.Model):
    _name = "sh.disease.crops"
    _description = "crops Disease"
    _rec_name = 'sh_disease_id'
    
    sh_disease_id = fields.Many2one('sh.disease',string="Disease", required=True)
    details = fields.Text(related='sh_disease_id.details', string="Details", readonly=False)

    symptoms = fields.Text(string="Symptoms")
    survival_and_spread = fields.Text(string="Survival and Spread")
    suitable_conditions = fields.Text(string="Suitable Conditions")
    cause_description = fields.Text(string="Cause Description")

    precautions = fields.Text(string="Precautions")
    medications = fields.Text(string="Test Medications")
    cure_description = fields.Text(string="Cure Description")


    sh_agri_crops_id = fields.Many2one("sh.agriculture.crops", string="Crop")
