# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_process_vehicles(models.Model):
    _name = "sh.process.vehicles"
    _description = "about vehicles"
    _rec_name = 'sh_agri_vehicles_id'

    sh_agri_vehicles_id = fields.Many2one(
        "sh.agri.vehicles", string="Fleet Vehicle", required=True)
    # total_vehicle = fields.Integer(
    #     related="sh_agri_vehicles_id.total_vehicle", string="Total Vehicle")
    begin_date = fields.Date(
        related="sh_agri_vehicles_id.begin_date", string="Begin Date")
    finish_date = fields.Date(
        related="sh_agri_vehicles_id.finish_date", string="Finish Date")
    description = fields.Text(
        related="sh_agri_vehicles_id.description", string="Description")
    
    sh_list_process_id = fields.Many2one("sh.list.process")

    project_task_id = fields.Many2one("project.task")
