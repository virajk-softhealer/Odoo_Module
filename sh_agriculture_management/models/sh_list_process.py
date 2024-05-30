# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_list_process(models.Model):
    _name = "sh.list.process"
    _description = "crops Process"
    _rec_name = 'sh_task_id'
    _order = 'crop_order_id, sequence, id'


    sh_task_id = fields.Many2one('project.task', string="Task Of Process", required=True)
    sh_duration = fields.Integer(string="Duration")
    sh_duration_day = fields.Char(default="days", string=" ", readonly=True)
   
    sh_agri_crops_id = fields.Many2one(
        "sh.agriculture.crops", string='Processes of Crop')
 
    sh_process_equipment_ids = fields.One2many(
        'sh.process.equipment', 'sh_list_process_id')

    sh_process_animals_ids = fields.One2many(
        'sh.process.animals', 'sh_list_process_id')
    
    sh_process_vehicles_ids = fields.One2many(
        'sh.process.vehicles', 'sh_list_process_id')
    
    sh_labour_ids = fields.One2many(
        'sh.labour', 'sh_list_process_id')

    crop_order_id = fields.Many2one("sh.crop.orders")
    sequence = fields.Integer(string="Sequence", default=10)

    # labours_total = fields.Integer(compute='_compute_labours_total')
    
   
    # @api.depends('sh_labour_ids')
    # def _compute_labours_total(self):
    #     for rec in self:
    #         rec.labours_total = 0
    #         labours = 0
    #         for lab in rec.sh_labour_ids:
    #             labours += lab.total_labour
    #         rec.labours_total = labours