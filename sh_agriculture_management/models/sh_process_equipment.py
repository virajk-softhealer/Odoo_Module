from odoo import fields, models, api

# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


class sh_process_equipment(models.Model):
    _name = "sh.process.equipment"
    _description = "process equipment"
    

    equipment = fields.Many2one("maintenance.equipment", string="Equipment", required=True)
    serial_no = fields.Char(string="Serial No")
    alloted_date = fields.Date(related='equipment.assign_date',string="Alloted Date")
    owner = fields.Many2one(related='equipment.owner_user_id', string="Owner")
    technician = fields.Many2one(related='equipment.technician_user_id', string="Technician")
    equipment_category = fields.Many2one(related='equipment.category_id',string="Equipment Category")
    
    sh_list_process_id = fields.Many2one(
        "sh.list.process")
    
    project_task_id = fields.Many2one(
        "project.task")

   
