# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api

class ShLabour(models.Model):
    _name = "sh.labour"
    _description = "about Labours"

    name = fields.Char( string="Labour Type", required=True)
    total_labour = fields.Integer(string="Total Labour")
    begin_date = fields.Date(string="Begin Date")
    finish_date = fields.Date(string="Finish Date")
    total_days = fields.Integer(string="Total Days")
    description = fields.Text( string="Description")
    
    sh_list_process_id = fields.Many2one(
        "sh.list.process")
    
    project_task_id = fields.Many2one(
        "project.task")


    @api.onchange('begin_date', 'finish_date')
    def _onchange_total_days(self):
        for rec in self:
            if rec.begin_date and rec.finish_date:
                delta = rec.finish_date - rec.begin_date
                rec.total_days = delta.days + 1
            else:
                rec.total_days = 0

    @api.onchange('begin_date', 'finish_date')
    def _onchange_dates(self):
        if self.begin_date and self.finish_date and self.begin_date > self.finish_date:
            self.begin_date, self.finish_date = self.finish_date, self.begin_date
