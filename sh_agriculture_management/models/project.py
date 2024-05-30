# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class sh_project(models.Model):
    _inherit = "project.project"

    sh_crop_order_id = fields.Many2one("sh.crop.orders", string="Crop Order")
    is_agri_project = fields.Boolean()

    def action_view_crop_order(self):
        self.ensure_one()
        # crop_order = self.env.ref(
        #     'sh_agriculture_management.sh_crop_orders_action').read()[0]
        crop_order = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_crop_orders_action")

        crop_order['domain'] = [
            ('name', '=',  self.sh_crop_order_id.name)]
        print("\n\n\n\n\n==========", crop_order['domain'])
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sh.crop.orders',
            'domain': crop_order['domain'],
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': False,
            "name": ("Crop Orders"),
            'target': 'sh_crop_orders_action',

        }

    def action_view_related_crop(self): 
        self.ensure_one()
        # related_crop = self.env.ref(
        #     'sh_agriculture_management.sh_agriculture_crops_action').read()[0]
        related_crop = self.env["ir.actions.actions"]._for_xml_id("sh_agriculture_management.sh_agriculture_crops_action")
        related_crop['domain'] = [
            ('product_id', '=',  self.sh_crop_order_id.sh_agriculture_crops_id.product_id.id)]
        print("\n\n\n\n\n==========", related_crop['domain'])
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sh.agriculture.crops',
            'domain': related_crop['domain'],
            'views': [(False, 'tree'), (False, 'form')],
            'view_id': False,
            "name": ("Related Crop"),
            'target': 'sh_agriculture_crops_action',

        }


class sh_task(models.Model):
    _inherit = "project.task"

    sh_crop_order_id = fields.Many2one(
        "sh.crop.orders", string="Crop Order")
    sh_agriculture_crops_id = fields.Many2one(
        "sh.agriculture.crops", string="Crop Order")
    
    is_agri_task = fields.Boolean()

    sh_process_equipment_ids = fields.One2many(
        'sh.process.equipment', 'project_task_id')

    sh_process_animals_ids = fields.One2many(
        'sh.process.animals', 'project_task_id')

    sh_process_vehicles_ids = fields.One2many(
        'sh.process.vehicles', 'project_task_id')
    
    sh_labour_ids = fields.One2many(
        'sh.labour', 'project_task_id')
    
  
