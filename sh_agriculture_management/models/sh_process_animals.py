from odoo import fields, models, api

# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


class sh_process_animals(models.Model):
    _name = "sh.process.animals"
    _description = "process equipment"

    animal_id = fields.Many2one("res.partner", string="Animal Name",
                                domain=[('animal', "=", True)], required=True)
    total_animal = fields.Integer(string="Total Animals")
    begin_date = fields.Date(string="Begin Date")
    finish_date = fields.Date(string="Finish Date")
    animal_description = fields.Text(string="Animal's Description")

    sh_list_process_id = fields.Many2one(
        "sh.list.process")
    
    project_task_id = fields.Many2one(
        "project.task")
