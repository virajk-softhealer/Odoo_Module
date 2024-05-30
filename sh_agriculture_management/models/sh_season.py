# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models,api


class ShSeason(models.Model):
    _name = "sh.season"
    _description = "Season"

    name = fields.Char(string="Season", required=True)
    begin_date = fields.Char(string="Begin Date")
    finish_date = fields.Char(string="Finish Date")
    # begin_date = fields.Date(string="Begin Date")
    # finish_date = fields.Date(string="Finish Date")
    description = fields.Text(string="Description")


    # @api.onchange('begin_date', 'finish_date')
    # def _onchange_dates(self):
    #     if self.begin_date and self.finish_date and self.begin_date > self.finish_date:
    #         self.begin_date, self.finish_date = self.finish_date, self.begin_date
